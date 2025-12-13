import pandas as pd
import requests
import io
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class AutoMpgDataset(BaseDatasetLoader):
    """Auto MPG dataset from UCI ML Repository for regression."""

    def get_dataset_info(self):
        return {
            'name': 'AutoMpgDataset',
            'source_id': 'uci:auto_mpg',
            'category': 'regression',
            'description': 'Auto MPG dataset: predict miles per gallon from car characteristics.',
            'target_column': 'mpg'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data"
        print(f"[{dataset_name}] Downloading from {url}")
        
        try:
            response = requests.get(url, timeout=30)
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}")
            return response.content
        except Exception as e:
            print(f"[{dataset_name}] Download failed: {e}")
            raise
    
    def process_dataframe(self, df, info):
        dataset_name = info['name']
        
        # Handle whitespace separated format
        if df.shape[1] == 1:
            lines = df.iloc[:, 0].astype(str).tolist()
            data = []
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 8:
                        data.append(parts[:8])
            df = pd.DataFrame(data)
        
        # Set column names
        df.columns = ['mpg', 'cylinders', 'displacement', 'horsepower', 'weight', 'acceleration', 'model_year', 'origin']
        
        # Convert to numeric, handle '?' as missing
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Set target
        df['target'] = df['mpg']
        df = df.drop('mpg', axis=1)
        
        # Ensure target is last column
        cols = [col for col in df.columns if col != 'target'] + ['target']
        df = df[cols]
        
        # Handle missing values
        df = df.fillna(df.median())
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[{dataset_name}] Final shape: {df.shape}, Target range: {df['target'].min():.1f}-{df['target'].max():.1f}")
        return df 

if __name__ == "__main__":
    ds = AutoMpgDataset()
    frame = ds.get_data()
    print(frame.head()) 
    # ------------------------------------------------------------------
    # Agent-aware feature engineering hooks (Auto MPG)
    # ------------------------------------------------------------------
    def get_feature_agent(self, provider: str = "GPT5"):
        return {"provider": provider, "name": "AutoMpgFeatureAgent", "version": "v1"}

    def _propose_agent_feature_plan(self, df: pd.DataFrame, agent) -> list:
        import numpy as np
        eps = 1e-6
        def has_all(cols):
            return all(c in df.columns for c in cols)
        plan = []

        # Power-to-weight ratio (key performance metric)
        if has_all(["horsepower", "weight"]):
            plan.append({"name": "power_weight_ratio", "requires": ["horsepower", "weight"],
                        "builder": lambda d: d["horsepower"] / (d["weight"] + eps)})
            plan.append({"name": "weight_per_hp", "requires": ["horsepower", "weight"],
                        "builder": lambda d: d["weight"] / (d["horsepower"] + eps)})
        
        # Engine efficiency features
        if has_all(["displacement", "cylinders"]):
            plan.append({"name": "displacement_per_cylinder", "requires": ["displacement", "cylinders"],
                        "builder": lambda d: d["displacement"] / (d["cylinders"] + eps)})
        
        if has_all(["displacement", "horsepower"]):
            plan.append({"name": "hp_per_liter", "requires": ["displacement", "horsepower"],
                        "builder": lambda d: d["horsepower"] / (d["displacement"] + eps)})
            plan.append({"name": "displacement_hp_ratio", "requires": ["displacement", "horsepower"],
                        "builder": lambda d: d["displacement"] / (d["horsepower"] + eps)})
        
        # Weight and size features
        if "weight" in df.columns:
            plan.append({"name": "weight_squared", "requires": ["weight"],
                        "builder": lambda d: (d["weight"] / 1000) ** 2})  # Scale down for numerical stability
            plan.append({"name": "weight_log", "requires": ["weight"],
                        "builder": lambda d: np.log(d["weight"])})
        
        # Acceleration features
        if has_all(["acceleration", "horsepower"]):
            plan.append({"name": "acceleration_hp_ratio", "requires": ["acceleration", "horsepower"],
                        "builder": lambda d: d["acceleration"] / (d["horsepower"] + eps)})
        
        if has_all(["acceleration", "weight"]):
            plan.append({"name": "acceleration_weight_product", "requires": ["acceleration", "weight"],
                        "builder": lambda d: d["acceleration"] * d["weight"] / 1000})
        
        # Model year era features
        if "model_year" in df.columns:
            plan.append({"name": "is_70s_car", "requires": ["model_year"],
                        "builder": lambda d: ((d["model_year"] >= 70) & (d["model_year"] < 80)).astype(int)})
            plan.append({"name": "is_80s_car", "requires": ["model_year"],
                        "builder": lambda d: (d["model_year"] >= 80).astype(int)})
            plan.append({"name": "years_since_70", "requires": ["model_year"],
                        "builder": lambda d: d["model_year"] - 70})
        
        # Origin-based features
        if "origin" in df.columns:
            plan.append({"name": "is_american", "requires": ["origin"],
                        "builder": lambda d: (d["origin"] == 1).astype(int)})
            plan.append({"name": "is_european", "requires": ["origin"],
                        "builder": lambda d: (d["origin"] == 2).astype(int)})
            plan.append({"name": "is_japanese", "requires": ["origin"],
                        "builder": lambda d: (d["origin"] == 3).astype(int)})
        
        # Era and technology interaction
        if has_all(["model_year", "cylinders"]):
            plan.append({"name": "era_cylinder_trend", "requires": ["model_year", "cylinders"],
                        "builder": lambda d: (d["model_year"] - 70) * (8 - d["cylinders"])})
        
        # Fuel efficiency predictors
        if has_all(["weight", "displacement", "cylinders"]):
            plan.append({"name": "fuel_inefficiency_index", "requires": ["weight", "displacement", "cylinders"],
                        "builder": lambda d: (d["weight"] * d["displacement"]) / (1000 * d["cylinders"])})
        
        # Performance class indicators
        if has_all(["horsepower", "acceleration"]):
            plan.append({"name": "performance_index", "requires": ["horsepower", "acceleration"],
                        "builder": lambda d: d["horsepower"] / d["acceleration"]})
        
        # Cylinder type features
        if "cylinders" in df.columns:
            plan.append({"name": "is_4cyl", "requires": ["cylinders"],
                        "builder": lambda d: (d["cylinders"] == 4).astype(int)})
            plan.append({"name": "is_6cyl", "requires": ["cylinders"],
                        "builder": lambda d: (d["cylinders"] == 6).astype(int)})
            plan.append({"name": "is_8cyl", "requires": ["cylinders"],
                        "builder": lambda d: (d["cylinders"] == 8).astype(int)})
        
        return plan

    @staticmethod
    def expand_features_on_dataframe(df: pd.DataFrame) -> (pd.DataFrame, list):
        self_like = AutoMpgDataset()
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
        df, added = AutoMpgDataset.expand_features_on_dataframe(df)
        try:
            df.attrs["agent_expansion_applied"] = True
            df.attrs["agent_provider"] = agent_provider
            df.attrs["agent_expanded_features"] = added
        except Exception:
            pass
        return df
