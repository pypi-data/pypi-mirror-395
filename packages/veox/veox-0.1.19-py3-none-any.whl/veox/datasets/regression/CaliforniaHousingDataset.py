import pandas as pd
import io
import numpy as np
from sklearn.datasets import fetch_california_housing
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class CaliforniaHousingDataset(BaseDatasetLoader):
    """
    Loader for the California Housing dataset from scikit-learn.
    
    This dataset has 20,640 observations on housing prices in California.
    The task is to predict the median house value for California districts.
    
    Features: 8 attributes including median income, housing median age, etc.
    Target: Median house value for California districts
    """

    def get_dataset_info(self):
        """Dataset metadata for the loader framework"""
        return {
            'name': 'CaliforniaHousingDataset',
            'source_id': 'sklearn:california_housing',  # Unique identifier
            'category': 'regression',
            'description': 'California Housing dataset: regression to predict median house values in California districts.'
        }
    
    def download_dataset(self, info):
        """Get the California Housing dataset from scikit-learn"""
        dataset_name = info['name']
        print(f"[{dataset_name}] Loading California Housing dataset from scikit-learn...")
        
        try:
            # Load the dataset from scikit-learn
            california = fetch_california_housing()
            
            # Create DataFrame
            df = pd.DataFrame(california.data, columns=california.feature_names)
            df["target"] = california.target
            
            # Convert to CSV bytes
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue().encode('utf-8')
            
            file_size = len(csv_data)
            print(f"[{dataset_name}] Dataset loaded. Size: {file_size} bytes")
            
            if file_size < 5000:
                print(f"[{dataset_name}] Data too small. First few rows:\n{df.head().to_string()}")
                raise Exception(f"Generated data too small: {file_size} bytes. Expected >5 KB.")
                
            return csv_data
        except Exception as e:
            print(f"[{dataset_name}] Loading failed: {str(e)}")
            raise
    
    def process_dataframe(self, df, info):
        """Process the dataset into final form"""
        dataset_name = info['name']
        
        print(f"[{dataset_name}] DataFrame shape: {df.shape}")
        print(f"[{dataset_name}] Data types of columns:\n{df.dtypes}")
        print(f"[{dataset_name}] First 5 rows:\n{df.head().to_string()}")
        
        # NOTE: All data cleaning, imputation, and shuffling steps have been removed to adhere to the
        # guideline that dataset loaders should not alter feature data.  The dataframe is returned
        # exactly as downloaded (aside from the optional prints above).
        
        # Attach lightweight attrs to help downstream expansion
        try:
            df.attrs["dataset_source"] = "CaliforniaHousingDataset"
            df.attrs["raw_feature_names"] = [c for c in df.columns if c != 'target']
            df.attrs["feature_expander"] = ("CaliforniaHousingDataset", "expand_features_on_dataframe")
        except Exception:
            pass
        
        return df

    # ------------------------------------------------------------------
    # Agent-aware feature engineering hooks (California Housing)
    # ------------------------------------------------------------------
    def get_feature_agent(self, provider: str = "GPT5"):
        return {"provider": provider, "name": "CaliforniaHousingFeatureAgent", "version": "v1"}

    def _propose_agent_feature_plan(self, df: pd.DataFrame, agent) -> list:
        eps = 1e-6
        def has_all(cols):
            return all(c in df.columns for c in cols)

        plan = []

        # Room density features
        if has_all(['AveRooms', 'AveBedrms']):
            plan.append({
                "name": "non_bedroom_rooms",
                "requires": ["AveRooms", "AveBedrms"],
                "builder": lambda d: d["AveRooms"] - d["AveBedrms"],
            })
            plan.append({
                "name": "bedroom_ratio",
                "requires": ["AveRooms", "AveBedrms"],
                "builder": lambda d: d["AveBedrms"] / (d["AveRooms"] + eps),
            })

        # Income features
        if has_all(["MedInc"]):
            plan.append({
                "name": "income_squared",
                "requires": ["MedInc"],
                "builder": lambda d: d["MedInc"] ** 2,
            })
            plan.append({
                "name": "income_log",
                "requires": ["MedInc"],
                "builder": lambda d: np.log1p(d["MedInc"]),
            })

        # Population density
        if has_all(["Population", "AveOccup"]):
            plan.append({
                "name": "total_households",
                "requires": ["Population", "AveOccup"],
                "builder": lambda d: d["Population"] / (d["AveOccup"] + eps),
            })

        # Age features
        if has_all(["HouseAge"]):
            plan.append({
                "name": "is_new",
                "requires": ["HouseAge"],
                "builder": lambda d: (d["HouseAge"] < 10).astype(float),
            })
            plan.append({
                "name": "is_old",
                "requires": ["HouseAge"],
                "builder": lambda d: (d["HouseAge"] > 30).astype(float),
            })

        # Location features
        if has_all(["Latitude", "Longitude"]):
            sf_lat, sf_lon = 37.7749, -122.4194  # San Francisco
            la_lat, la_lon = 34.0522, -118.2437  # Los Angeles
            plan.append({
                "name": "dist_to_sf",
                "requires": ["Latitude", "Longitude"],
                "builder": lambda d: np.sqrt((d["Latitude"] - sf_lat)**2 + (d["Longitude"] - sf_lon)**2),
            })
            plan.append({
                "name": "dist_to_la",
                "requires": ["Latitude", "Longitude"],
                "builder": lambda d: np.sqrt((d["Latitude"] - la_lat)**2 + (d["Longitude"] - la_lon)**2),
            })
            plan.append({
                "name": "coastal_proximity",
                "requires": ["Longitude"],
                "builder": lambda d: np.abs(d["Longitude"] + 120),
            })

        # Interaction features
        if has_all(["MedInc", "AveRooms"]):
            plan.append({
                "name": "income_x_rooms",
                "requires": ["MedInc", "AveRooms"],
                "builder": lambda d: d["MedInc"] * d["AveRooms"],
            })

        # ---------------- Additional high-gain derived features (base-columns only) ----------------
        # Additional city distances and geographic composites
        if has_all(["Latitude", "Longitude"]):
            sd_lat, sd_lon = 32.7157, -117.1611  # San Diego
            sj_lat, sj_lon = 37.3382, -121.8863  # San Jose
            plan.append({
                "name": "dist_to_sd",
                "requires": ["Latitude", "Longitude"],
                "builder": lambda d: np.sqrt((d["Latitude"] - sd_lat)**2 + (d["Longitude"] - sd_lon)**2),
            })
            plan.append({
                "name": "dist_to_sj",
                "requires": ["Latitude", "Longitude"],
                "builder": lambda d: np.sqrt((d["Latitude"] - sj_lat)**2 + (d["Longitude"] - sj_lon)**2),
            })
            # Min/mean distance to major hubs computed directly from lat/lon
            plan.append({
                "name": "min_city_dist",
                "requires": ["Latitude", "Longitude"],
                "builder": lambda d: pd.concat([
                    np.sqrt((d["Latitude"] - 37.7749)**2 + (d["Longitude"] + 122.4194)**2),  # SF
                    np.sqrt((d["Latitude"] - 34.0522)**2 + (d["Longitude"] + 118.2437)**2),  # LA
                    np.sqrt((d["Latitude"] - 32.7157)**2 + (d["Longitude"] + 117.1611)**2),  # SD
                    np.sqrt((d["Latitude"] - 37.3382)**2 + (d["Longitude"] + 121.8863)**2),  # SJ
                ], axis=1).min(axis=1),
            })
            plan.append({
                "name": "mean_city_dist",
                "requires": ["Latitude", "Longitude"],
                "builder": lambda d: pd.concat([
                    np.sqrt((d["Latitude"] - 37.7749)**2 + (d["Longitude"] + 122.4194)**2),
                    np.sqrt((d["Latitude"] - 34.0522)**2 + (d["Longitude"] + 118.2437)**2),
                    np.sqrt((d["Latitude"] - 32.7157)**2 + (d["Longitude"] + 117.1611)**2),
                    np.sqrt((d["Latitude"] - 37.3382)**2 + (d["Longitude"] + 121.8863)**2),
                ], axis=1).mean(axis=1),
            })
            plan.append({
                "name": "Latitude_per_Longitude",
                "requires": ["Latitude", "Longitude"],
                "builder": lambda d: d["Latitude"] / (np.abs(d["Longitude"]) + eps),
            })
            plan.append({
                "name": "lat_squared",
                "requires": ["Latitude"],
                "builder": lambda d: d["Latitude"] ** 2,
            })
            plan.append({
                "name": "lon_squared",
                "requires": ["Longitude"],
                "builder": lambda d: d["Longitude"] ** 2,
            })
            plan.append({
                "name": "lat_lon_product",
                "requires": ["Latitude", "Longitude"],
                "builder": lambda d: d["Latitude"] * d["Longitude"],
            })

        # Richer income transforms and ratios
        if has_all(["MedInc"]):
            plan.append({
                "name": "income_sqrt",
                "requires": ["MedInc"],
                "builder": lambda d: np.sqrt(np.clip(d["MedInc"], a_min=0, a_max=None)),
            })
            plan.append({
                "name": "income_cubed",
                "requires": ["MedInc"],
                "builder": lambda d: d["MedInc"] ** 3,
            })

        if has_all(["MedInc", "HouseAge"]):
            plan.append({
                "name": "income_x_age",
                "requires": ["MedInc", "HouseAge"],
                "builder": lambda d: d["MedInc"] * d["HouseAge"],
            })
            plan.append({
                "name": "income_per_age",
                "requires": ["MedInc", "HouseAge"],
                "builder": lambda d: d["MedInc"] / (d["HouseAge"] + 1.0),
            })

        if has_all(["MedInc", "AveOccup"]):
            plan.append({
                "name": "income_per_occup",
                "requires": ["MedInc", "AveOccup"],
                "builder": lambda d: d["MedInc"] / (d["AveOccup"] + eps),
            })

        if has_all(["MedInc", "AveRooms"]):
            plan.append({
                "name": "income_per_room",
                "requires": ["MedInc", "AveRooms"],
                "builder": lambda d: d["MedInc"] / (d["AveRooms"] + eps),
            })

        if has_all(["MedInc", "Latitude", "Longitude"]):
            # Income per (min distance to hubs) computed directly to avoid dependency ordering
            plan.append({
                "name": "income_per_city_dist",
                "requires": ["MedInc", "Latitude", "Longitude"],
                "builder": lambda d: d["MedInc"] / (pd.concat([
                    np.sqrt((d["Latitude"] - 37.7749)**2 + (d["Longitude"] + 122.4194)**2),
                    np.sqrt((d["Latitude"] - 34.0522)**2 + (d["Longitude"] + 118.2437)**2),
                    np.sqrt((d["Latitude"] - 32.7157)**2 + (d["Longitude"] + 117.1611)**2),
                    np.sqrt((d["Latitude"] - 37.3382)**2 + (d["Longitude"] + 121.8863)**2),
                ], axis=1).min(axis=1) + eps),
            })

        # ---------------- Best-performing derivatives (compute directly from base columns) ----------------
        # IPO = income_per_occup and its transforms/interactions
        if has_all(["MedInc", "AveOccup"]):
            plan.append({
                "name": "income_per_occup_log",
                "requires": ["MedInc", "AveOccup"],
                "builder": lambda d: np.log1p(d["MedInc"] / (d["AveOccup"] + eps)),
            })
            plan.append({
                "name": "income_per_occup_sqrt",
                "requires": ["MedInc", "AveOccup"],
                "builder": lambda d: np.sqrt(np.clip(d["MedInc"] / (d["AveOccup"] + eps), a_min=0, a_max=None)),
            })
            plan.append({
                "name": "income_per_occup_sq",
                "requires": ["MedInc", "AveOccup"],
                "builder": lambda d: (d["MedInc"] / (d["AveOccup"] + eps)) ** 2,
            })
            plan.append({
                "name": "income_per_occup_inv",
                "requires": ["MedInc", "AveOccup"],
                "builder": lambda d: 1.0 / (d["MedInc"] / (d["AveOccup"] + eps) + eps),
            })

        if has_all(["MedInc", "AveOccup", "Latitude", "Longitude"]):
            plan.append({
                "name": "ipo_x_latlon",
                "requires": ["MedInc", "AveOccup", "Latitude", "Longitude"],
                "builder": lambda d: (d["MedInc"] / (d["AveOccup"] + eps)) * (d["Latitude"] / (np.abs(d["Longitude"]) + eps)),
            })
            plan.append({
                "name": "income_x_income_per_occup",
                "requires": ["MedInc", "AveOccup"],
                "builder": lambda d: d["MedInc"] * (d["MedInc"] / (d["AveOccup"] + eps)),
            })

        # Income per room refinements
        if has_all(["MedInc", "AveRooms"]):
            plan.append({
                "name": "income_per_room_log",
                "requires": ["MedInc", "AveRooms"],
                "builder": lambda d: np.log1p(d["MedInc"] / (d["AveRooms"] + eps)),
            })
            plan.append({
                "name": "income_per_room_sq",
                "requires": ["MedInc", "AveRooms"],
                "builder": lambda d: (d["MedInc"] / (d["AveRooms"] + eps)) ** 2,
            })

        # City distance ratio family and interactions
        if has_all(["Latitude", "Longitude"]):
            def _min_city_dist_local(d):
                return pd.concat([
                    np.sqrt((d["Latitude"] - 37.7749)**2 + (d["Longitude"] + 122.4194)**2),
                    np.sqrt((d["Latitude"] - 34.0522)**2 + (d["Longitude"] + 118.2437)**2),
                    np.sqrt((d["Latitude"] - 32.7157)**2 + (d["Longitude"] + 117.1611)**2),
                    np.sqrt((d["Latitude"] - 37.3382)**2 + (d["Longitude"] + 121.8863)**2),
                ], axis=1).min(axis=1)
            def _mean_city_dist_local(d):
                return pd.concat([
                    np.sqrt((d["Latitude"] - 37.7749)**2 + (d["Longitude"] + 122.4194)**2),
                    np.sqrt((d["Latitude"] - 34.0522)**2 + (d["Longitude"] + 118.2437)**2),
                    np.sqrt((d["Latitude"] - 32.7157)**2 + (d["Longitude"] + 117.1611)**2),
                    np.sqrt((d["Latitude"] - 37.3382)**2 + (d["Longitude"] + 121.8863)**2),
                ], axis=1).mean(axis=1)

            plan.append({
                "name": "min_over_mean_city_dist",
                "requires": ["Latitude", "Longitude"],
                "builder": lambda d: _min_city_dist_local(d) / (_mean_city_dist_local(d) + eps),
            })
            plan.append({
                "name": "log_min_over_mean_city_dist",
                "requires": ["Latitude", "Longitude"],
                "builder": lambda d: np.log1p(_min_city_dist_local(d) / (_mean_city_dist_local(d) + eps)),
            })
            plan.append({
                "name": "min_over_mean_city_dist_sq",
                "requires": ["Latitude", "Longitude"],
                "builder": lambda d: ( _min_city_dist_local(d) / (_mean_city_dist_local(d) + eps) ) ** 2,
            })

        if has_all(["MedInc", "Latitude", "Longitude"]):
            plan.append({
                "name": "MedInc_x_log_min_over_mean_city_dist",
                "requires": ["MedInc", "Latitude", "Longitude"],
                "builder": lambda d: d["MedInc"] * np.log1p(_min_city_dist_local(d) / (_mean_city_dist_local(d) + eps)),
            })
            plan.append({
                "name": "MedInc_x_min_over_mean_city_dist",
                "requires": ["MedInc", "Latitude", "Longitude"],
                "builder": lambda d: d["MedInc"] * (_min_city_dist_local(d) / (_mean_city_dist_local(d) + eps)),
            })

        if has_all(["MedInc", "AveOccup", "Latitude", "Longitude"]):
            plan.append({
                "name": "ipo_x_minmean_sq",
                "requires": ["MedInc", "AveOccup", "Latitude", "Longitude"],
                "builder": lambda d: (d["MedInc"] / (d["AveOccup"] + eps)) * ( (_min_city_dist_local(d) / (_mean_city_dist_local(d) + eps)) ** 2 ),
            })

        # Coastal refinements
        if has_all(["Longitude"]):
            plan.append({
                "name": "coastal_proximity_sq",
                "requires": ["Longitude"],
                "builder": lambda d: (np.abs(d["Longitude"] + 120)) ** 2,
            })
            plan.append({
                "name": "coastal_proximity_log",
                "requires": ["Longitude"],
                "builder": lambda d: np.log1p(np.abs(d["Longitude"] + 120)),
            })

        return plan

    @staticmethod
    def expand_features_on_dataframe(df: pd.DataFrame) -> (pd.DataFrame, list):
        self_like = CaliforniaHousingDataset()
        agent = self_like.get_feature_agent(provider="GPT5")
        plan = self_like._propose_agent_feature_plan(df, agent)
        added = []
        for item in plan:
            name = item["name"]
            requires = item["requires"]
            builder = item["builder"]
            if name in df.columns:
                continue
            if all(col in df.columns for col in requires):
                try:
                    df[name] = builder(df)
                    added.append(name)
                except Exception:
                    pass
        return df, added

    def get_data_gen(self, agent_provider: str = "GPT5", force: bool = False) -> pd.DataFrame:
        df = self.get_data()
        if isinstance(df, pd.DataFrame) and df.attrs.get("agent_expansion_applied") and not force:
            return df
        agent = self.get_feature_agent(provider=agent_provider)
        plan = self._propose_agent_feature_plan(df, agent)
        df, added = self.expand_features_on_dataframe(df)
        try:
            df.attrs["agent_expansion_applied"] = True
            df.attrs["agent_provider"] = agent_provider
            df.attrs["agent_expanded_features"] = added
        except Exception:
            pass
        return df

# For testing
if __name__ == "__main__":
    dataset = CaliforniaHousingDataset()
    df = dataset.get_data()
    print(f"Dataset loaded successfully with {len(df)} rows.")
    
    # Test expansion
    df_exp = dataset.get_data_gen()
    print(f"Expanded dataset has {len(df_exp.columns)} columns")

    # 5-fold R^2 comparison (baseline vs AgentFeatureExpander)
    try:
        from sklearn.model_selection import KFold
        from sklearn.metrics import r2_score, mean_squared_error
        from catboost import CatBoostRegressor
        from app.seed_data.Generative.shared.stages.transforms.expanders.AgentFeatureExpander import AgentFeatureExpander

        X_base = df.drop(columns=["target"])
        y = df["target"]

        kf = KFold(n_splits=5, shuffle=True, random_state=42)
        r2s_base = []
        r2s_exp = []
        mses_base = []
        mses_exp = []

        print("\nBaseline (no expander) 5-fold R^2:")
        for fold_idx, (train_idx, test_idx) in enumerate(kf.split(X_base)):
            Xtr = X_base.iloc[train_idx]
            Xte = X_base.iloc[test_idx]
            ytr = y.iloc[train_idx]
            yte = y.iloc[test_idx]

            model = CatBoostRegressor(verbose=False, depth=8, learning_rate=0.07, iterations=900, l2_leaf_reg=4.0, loss_function="RMSE", random_seed=42)
            model.fit(Xtr, ytr)
            p = model.predict(Xte)
            r2 = r2_score(yte, p)
            mse = mean_squared_error(yte, p)
            r2s_base.append(r2)
            mses_base.append(mse)
            print(f"Fold {fold_idx}: R2={r2:.6f} MSE={mse:.6f}")

        print("\nAgent-expanded 5-fold R^2:")
        kf = KFold(n_splits=5, shuffle=True, random_state=42)
        for fold_idx, (train_idx, test_idx) in enumerate(kf.split(X_base)):
            Xtr2 = X_base.iloc[train_idx].copy()
            Xte2 = X_base.iloc[test_idx].copy()
            ytr2 = y.iloc[train_idx]
            yte2 = y.iloc[test_idx]

            expander = AgentFeatureExpander(prefer_dataset="CaliforniaHousingDataset")
            Xtr2 = expander.fit_transform(Xtr2, ytr2)
            Xte2 = expander.transform(Xte2)

            model2 = CatBoostRegressor(verbose=False, depth=8, learning_rate=0.07, iterations=900, l2_leaf_reg=4.0, loss_function="RMSE", random_seed=42)
            model2.fit(Xtr2.drop(columns=["target"]) if "target" in Xtr2.columns else Xtr2, ytr2)
            p2 = model2.predict(Xte2.drop(columns=["target"]) if "target" in Xte2.columns else Xte2)
            r2_2 = r2_score(yte2, p2)
            mse_2 = mean_squared_error(yte2, p2)
            r2s_exp.append(r2_2)
            mses_exp.append(mse_2)
            print(f"Fold {fold_idx}: R2={r2_2:.6f} MSE={mse_2:.6f}")

        print({
            "baseline_r2_mean": float(np.mean(r2s_base)),
            "baseline_r2_std": float(np.std(r2s_base)),
            "expanded_r2_mean": float(np.mean(r2s_exp)),
            "expanded_r2_std": float(np.std(r2s_exp)),
            "baseline_mse_mean": float(np.mean(mses_base)),
            "expanded_mse_mean": float(np.mean(mses_exp)),
            "folds": len(r2s_base),
        })
    except Exception as e:
        print(f"[CaliforniaHousingDataset] CV run skipped due to: {e}")

