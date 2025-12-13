import os
import pandas as pd
import io
import numpy as np
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class BostonHousingDataset(BaseDatasetLoader):
    """
    Boston Housing dataset loaded from scikit-learn.
    Example regression dataset with housing prices.
    
    Note: This dataset has ethical concerns as noted by scikit-learn's maintainers.
    This implementation is for educational purposes only.
    """
    
    def get_dataset_info(self):
        """Dataset metadata for the loader framework"""
        return {
            'name': 'BostonHousingDataset',
            'source_id': 'sklearn:boston_housing',  # Use sklearn source 
            'category': 'regression',
            'description': 'Boston Housing dataset: regression task to predict median house value in Boston suburbs.'
        }
    
    def download_dataset(self, info):
        """Get Boston Housing dataset from scikit-learn"""
        dataset_name = info['name']
        print(f"[{dataset_name}] Loading Boston Housing dataset from scikit-learn...")
        
        try:
            # Use scikit-learn's dataset since it's more reliable
            from sklearn.datasets import load_boston
            
            # Load the dataset
            boston = load_boston()
            
            # Create DataFrame
            feature_names = boston.feature_names
            df = pd.DataFrame(boston.data, columns=feature_names)
            df["target"] = boston.target
            
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
            
        except ImportError:
            # Fallback: create synthetic Boston-like dataset
            print(f"[{dataset_name}] sklearn not available, creating synthetic Boston housing data...")
            
            np.random.seed(42)
            n_samples = 506
            n_features = 13
            
            # Create synthetic features with reasonable ranges
            data = np.random.randn(n_samples, n_features)
            # Scale features to reasonable ranges
            data[:, 0] *= 10    # CRIM: crime rate
            data[:, 1] = np.random.uniform(0, 100, n_samples)  # ZN: residential land
            data[:, 2] = np.random.uniform(0, 30, n_samples)   # INDUS: industrial 
            data[:, 3] = np.random.binomial(1, 0.1, n_samples) # CHAS: river
            data[:, 4] = np.random.uniform(0.3, 0.9, n_samples) # NOX: pollution
            data[:, 5] = np.random.uniform(3, 9, n_samples)     # RM: rooms
            data[:, 6] = np.random.uniform(0, 100, n_samples)   # AGE: age
            data[:, 7] = np.random.uniform(1, 15, n_samples)    # DIS: distance
            data[:, 8] = np.random.randint(1, 25, n_samples)    # RAD: highways
            data[:, 9] = np.random.uniform(150, 700, n_samples) # TAX: tax rate
            data[:, 10] = np.random.uniform(10, 25, n_samples)  # PTRATIO: pupil-teacher
            data[:, 11] = np.random.uniform(300, 400, n_samples) # B: black population
            data[:, 12] = np.random.uniform(1, 35, n_samples)   # LSTAT: lower status
            
            # Create synthetic target (housing prices)
            target = (
                20 + 
                data[:, 5] * 5 +           # rooms matter most
                -data[:, 0] * 0.1 +        # crime decreases price
                -data[:, 12] * 0.3 +       # lower status decreases price
                data[:, 7] * 0.2 +         # distance from employment
                np.random.randn(n_samples) * 2  # noise
            )
            target = np.clip(target, 5, 50)  # Reasonable price range
            
            # Feature names
            feature_names = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 
                            'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT']
            
            # Create DataFrame
            df = pd.DataFrame(data, columns=feature_names)
            df["target"] = target
            
            # Convert to CSV bytes
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue().encode('utf-8')
            
            print(f"[{dataset_name}] Synthetic dataset created. Size: {len(csv_data)} bytes")
            return csv_data
            
        except Exception as e:
            print(f"[{dataset_name}] Loading failed: {str(e)}")
            raise
    
    def process_dataframe(self, df, info):
        """Process the dataset"""
        dataset_name = info['name']
        
        # Log basic stats
        print(f"[{dataset_name}] Loaded dataset with shape: {df.shape}")
        print(f"[{dataset_name}] Columns: {', '.join(df.columns)}")
        
        # Check for missing values
        missing_vals = df.isna().sum()
        print(f"[{dataset_name}] Missing values per column:")
        for col, count in missing_vals.items():
            if count > 0:
                print(f"  - {col}: {count} missing values ({100 * count / len(df):.2f}%)")
        
        # Rename target column if needed
        if 'MEDV' in df.columns and 'target' not in df.columns:
            df = df.rename(columns={'MEDV': 'target'})
            print(f"[{dataset_name}] Renamed 'MEDV' to 'target'")
        
        # Shuffle dataset
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        print(f"[{dataset_name}] Dataset shuffled and indices reset")
        
        return df

# For testing
if __name__ == "__main__":
    dataset = BostonHousingDataset()
    df = dataset.get_data()
    print(f"Dataset loaded with {len(df)} rows and {len(df.columns)} columns")

    # ------------------------------------------------------------------
    # Agent-aware feature engineering hooks (Boston Housing)
    # ------------------------------------------------------------------
    def get_feature_agent(self, provider: str = "GPT5"):
        return {"provider": provider, "name": "BostonHousingFeatureAgent", "version": "v1"}

    def _propose_agent_feature_plan(self, df: pd.DataFrame, agent) -> list:
        import numpy as np
        eps = 1e-6
        def has_all(cols):
            return all(c in df.columns for c in cols)
        plan = []

        # Crime-related features
        if "CRIM" in df.columns:
            plan.append({"name": "crime_log", "requires": ["CRIM"],
                        "builder": lambda d: np.log1p(d["CRIM"])})
            plan.append({"name": "high_crime", "requires": ["CRIM"],
                        "builder": lambda d: (d["CRIM"] > d["CRIM"].median()).astype(int)})
        
        # Room features
        if has_all(["RM", "AGE"]):
            plan.append({"name": "rooms_per_age", "requires": ["RM", "AGE"],
                        "builder": lambda d: d["RM"] / (d["AGE"] + 1)})
            plan.append({"name": "large_old_house", "requires": ["RM", "AGE"],
                        "builder": lambda d: ((d["RM"] > 6) & (d["AGE"] > 50)).astype(int)})
        
        # Accessibility features
        if has_all(["DIS", "RAD"]):
            plan.append({"name": "accessibility_index", "requires": ["DIS", "RAD"],
                        "builder": lambda d: d["RAD"] / (d["DIS"] + eps)})
            plan.append({"name": "dis_squared", "requires": ["DIS"],
                        "builder": lambda d: d["DIS"] ** 2})
        
        # Industrial and pollution
        if has_all(["INDUS", "NOX"]):
            plan.append({"name": "pollution_index", "requires": ["INDUS", "NOX"],
                        "builder": lambda d: d["INDUS"] * d["NOX"]})
            plan.append({"name": "indus_per_nox", "requires": ["INDUS", "NOX"],
                        "builder": lambda d: d["INDUS"] / (d["NOX"] + eps)})
        
        # Tax and property value
        if has_all(["TAX", "PTRATIO"]):
            plan.append({"name": "tax_per_student", "requires": ["TAX", "PTRATIO"],
                        "builder": lambda d: d["TAX"] / (d["PTRATIO"] + eps)})
            plan.append({"name": "tax_ptratio_product", "requires": ["TAX", "PTRATIO"],
                        "builder": lambda d: d["TAX"] * d["PTRATIO"] / 1000})
        
        # Socioeconomic features
        if has_all(["LSTAT", "RM"]):
            plan.append({"name": "status_room_ratio", "requires": ["LSTAT", "RM"],
                        "builder": lambda d: d["LSTAT"] / (d["RM"] + eps)})
            plan.append({"name": "luxury_indicator", "requires": ["LSTAT", "RM"],
                        "builder": lambda d: ((d["LSTAT"] < 10) & (d["RM"] > 7)).astype(int)})
        
        # Charles River dummy interaction
        if has_all(["CHAS", "DIS"]):
            plan.append({"name": "river_distance", "requires": ["CHAS", "DIS"],
                        "builder": lambda d: d["CHAS"] * d["DIS"]})
        
        # Age and condition
        if has_all(["AGE", "B"]):
            plan.append({"name": "age_b_ratio", "requires": ["AGE", "B"],
                        "builder": lambda d: d["AGE"] / (d["B"] + eps)})
        
        # Zoning features
        if "ZN" in df.columns:
            plan.append({"name": "has_zoning", "requires": ["ZN"],
                        "builder": lambda d: (d["ZN"] > 0).astype(int)})
            plan.append({"name": "zn_log", "requires": ["ZN"],
                        "builder": lambda d: np.log1p(d["ZN"])})
        
        # Combined quality index
        if has_all(["RM", "LSTAT", "PTRATIO"]):
            plan.append({"name": "quality_index", "requires": ["RM", "LSTAT", "PTRATIO"],
                        "builder": lambda d: (d["RM"] * 10) / ((d["LSTAT"] + 1) * (d["PTRATIO"] + 1))})
        
        return plan

    @staticmethod
    def expand_features_on_dataframe(df: pd.DataFrame) -> (pd.DataFrame, list):
        self_like = BostonHousingDataset()
        agent = self_like.get_feature_agent(provider="GPT5")
        plan = self_like._propose_agent_feature_plan(df, agent)
        added = []
        for item in plan:
            name = item["name"]; requires = item["requires"]; builder = item["builder"]
            if name in df.columns:
                continue
            if all(col in df.columns for col in requires):
                try:
                    df[name] = builder(df); added.append(name)
                except Exception:
                    pass
        return df, added

    def get_data_gen(self, agent_provider: str = "GPT5", force: bool = False) -> pd.DataFrame:
        df = self.get_data()
        if isinstance(df, pd.DataFrame) and df.attrs.get("agent_expansion_applied") and not force:
            return df
        agent = self.get_feature_agent(provider=agent_provider)
        plan = self._propose_agent_feature_plan(df, agent)
        df, added = BostonHousingDataset.expand_features_on_dataframe(df)
        try:
            df.attrs["agent_expansion_applied"] = True
            df.attrs["agent_provider"] = agent_provider
            df.attrs["agent_expanded_features"] = added
        except Exception:
            pass
        return df
