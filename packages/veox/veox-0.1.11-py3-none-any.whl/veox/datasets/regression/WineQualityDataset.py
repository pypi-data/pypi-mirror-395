import os
import pandas as pd
import requests
import io
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class WineQualityDataset(BaseDatasetLoader):
    """
    Loader for the Wine Quality dataset from the UCI Machine Learning Repository.
    
    This dataset contains physicochemical properties of red and white wines,
    with quality ratings that can be used for regression tasks.
    
    Features include alcohol content, acidity, pH, and other chemical properties.
    Target is the wine quality rating (continuous score from 0-10).
    """

    def get_dataset_info(self):
        """Dataset metadata for the loader framework"""
        return {
            'name': 'WineQualityDataset',
            'source_id': 'uci:wine_quality_regression',  # Unique identifier
            'category': 'regression',
            'description': 'Wine Quality dataset: regression to predict wine quality rating based on chemical properties.',
        }
    
    def download_dataset(self, info):
        """Download dataset from UCI repository"""
        dataset_name = info['name']
        # URL for the Wine Quality dataset (red wine variant)
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
        print(f"[{dataset_name}] Downloading from URL: {url}")
        
        try:
            r = requests.get(url, timeout=30)
            print(f"[{dataset_name}] HTTP response status: {r.status_code}")
            if r.status_code != 200:
                raise Exception(f"Failed to download dataset: HTTP {r.status_code}")
            
            file_size = len(r.content)
            print(f"[{dataset_name}] Download complete. File size: {file_size} bytes")
            
            if file_size < 10000:  # Sanity check for file size
                first_lines = r.content.decode("utf-8", errors="replace").splitlines()[:5]
                print(f"[{dataset_name}] File too small. First few lines:\n{os.linesep.join(first_lines)}")
                raise Exception(f"Downloaded file too small: {file_size} bytes. Expected >10 KB.")
                
            return r.content
        except Exception as e:
            print(f"[{dataset_name}] Download failed: {str(e)}")
            raise
    
    def process_dataframe(self, df, info):
        """Process the dataset into final form"""
        dataset_name = info['name']
        
        print(f"[{dataset_name}] DataFrame shape: {df.shape}")
        print(f"[{dataset_name}] Data types of columns:\n{df.dtypes}")
        print(f"[{dataset_name}] First 5 rows:\n{df.head().to_string()}")
        
        # Rename the quality column to 'target' for consistency with other datasets
        if 'quality' in df.columns and 'target' not in df.columns:
            df = df.rename(columns={'quality': 'target'})
            print(f"[{dataset_name}] Renamed 'quality' to 'target'")
        
        # Check for missing values
        print(f"[{dataset_name}] Checking for missing values:")
        for col in df.columns:
            missing = df[col].isna().sum()
            print(f"  - {col}: {missing} missing")
        
        # Fill missing values if any
        if df.isna().any().any():
            print(f"[{dataset_name}] Filling missing values with column medians...")
            for col in df.columns:
                if df[col].isna().any():
                    df[col] = df[col].fillna(df[col].median())
        
        # Shuffle dataset
        print(f"[{dataset_name}] Shuffling the dataset randomly...")
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        print(f"[{dataset_name}] Dataset shuffled and indices reset.")
        
        # Final logging
        print(f"[{dataset_name}] Final DataFrame shape: {df.shape}")
        print(f"[{dataset_name}] Target summary:")
        print(f"  - Mean: {df['target'].mean():.2f}")
        print(f"  - Std: {df['target'].std():.2f}")
        print(f"  - Min: {df['target'].min():.2f}")
        print(f"  - Max: {df['target'].max():.2f}")
        print(f"[{dataset_name}] Sample of first 5 rows:\n{df.head().to_string()}")
        
        return df

# For testing
if __name__ == "__main__":
    dataset = WineQualityDataset()
    df = dataset.get_data()
    print(f"Dataset loaded successfully with {len(df)} rows.") 
    # ------------------------------------------------------------------
    # Agent-aware feature engineering hooks (Wine Quality)
    # ------------------------------------------------------------------
    def get_feature_agent(self, provider: str = "GPT5"):
        return {"provider": provider, "name": "WineQualityFeatureAgent", "version": "v1"}

    def _propose_agent_feature_plan(self, df: pd.DataFrame, agent) -> list:
        import numpy as np
        eps = 1e-6
        def has_all(cols):
            return all(c in df.columns for c in cols)
        plan = []

        # Acidity features
        if has_all(["fixed_acidity", "volatile_acidity"]):
            plan.append({"name": "total_acidity", "requires": ["fixed_acidity", "volatile_acidity"],
                        "builder": lambda d: d["fixed_acidity"] + d["volatile_acidity"]})
            plan.append({"name": "acidity_ratio", "requires": ["fixed_acidity", "volatile_acidity"],
                        "builder": lambda d: d["fixed_acidity"] / (d["volatile_acidity"] + eps)})
        
        # pH-related features
        if "pH" in df.columns:
            plan.append({"name": "acidity_from_pH", "requires": ["pH"],
                        "builder": lambda d: 10 ** (-d["pH"])})
            plan.append({"name": "pH_squared", "requires": ["pH"],
                        "builder": lambda d: d["pH"] ** 2})
        
        # Sugar-acid balance
        if has_all(["residual_sugar", "fixed_acidity"]):
            plan.append({"name": "sugar_acid_ratio", "requires": ["residual_sugar", "fixed_acidity"],
                        "builder": lambda d: d["residual_sugar"] / (d["fixed_acidity"] + eps)})
        
        if has_all(["residual_sugar", "citric_acid"]):
            plan.append({"name": "sugar_citric_ratio", "requires": ["residual_sugar", "citric_acid"],
                        "builder": lambda d: d["residual_sugar"] / (d["citric_acid"] + eps)})
        
        # Sulfur dioxide features
        if has_all(["free_sulfur_dioxide", "total_sulfur_dioxide"]):
            plan.append({"name": "bound_sulfur_dioxide", "requires": ["free_sulfur_dioxide", "total_sulfur_dioxide"],
                        "builder": lambda d: d["total_sulfur_dioxide"] - d["free_sulfur_dioxide"]})
            plan.append({"name": "free_sulfur_ratio", "requires": ["free_sulfur_dioxide", "total_sulfur_dioxide"],
                        "builder": lambda d: d["free_sulfur_dioxide"] / (d["total_sulfur_dioxide"] + eps)})
        
        # Alcohol-density relationship
        if has_all(["alcohol", "density"]):
            plan.append({"name": "alcohol_density_index", "requires": ["alcohol", "density"],
                        "builder": lambda d: d["alcohol"] * (1 - d["density"])})
        
        # Salt-acid interaction
        if has_all(["chlorides", "fixed_acidity"]):
            plan.append({"name": "salt_acid_interaction", "requires": ["chlorides", "fixed_acidity"],
                        "builder": lambda d: d["chlorides"] * d["fixed_acidity"]})
        
        # Sulfates features
        if has_all(["sulphates", "alcohol"]):
            plan.append({"name": "sulphates_alcohol_ratio", "requires": ["sulphates", "alcohol"],
                        "builder": lambda d: d["sulphates"] / (d["alcohol"] + eps)})
        
        # Wine balance indicators
        if has_all(["pH", "alcohol", "residual_sugar"]):
            plan.append({"name": "wine_balance_index", "requires": ["pH", "alcohol", "residual_sugar"],
                        "builder": lambda d: (d["pH"] * d["alcohol"]) / (d["residual_sugar"] + 1)})
        
        # Volatile compounds
        if has_all(["volatile_acidity", "alcohol"]):
            plan.append({"name": "volatile_alcohol_ratio", "requires": ["volatile_acidity", "alcohol"],
                        "builder": lambda d: d["volatile_acidity"] / (d["alcohol"] + eps)})
        
        # Quality predictors from domain knowledge
        if has_all(["citric_acid", "volatile_acidity", "sulphates"]):
            plan.append({"name": "quality_index", "requires": ["citric_acid", "volatile_acidity", "sulphates"],
                        "builder": lambda d: (d["citric_acid"] + d["sulphates"]) / (d["volatile_acidity"] + eps)})
        
        # Density-based features
        if has_all(["density", "alcohol", "residual_sugar"]):
            plan.append({"name": "density_deviation", "requires": ["density", "alcohol", "residual_sugar"],
                        "builder": lambda d: d["density"] - (1 - 0.002 * d["alcohol"] + 0.0004 * d["residual_sugar"])})
        
        return plan

    @staticmethod
    def expand_features_on_dataframe(df: pd.DataFrame) -> (pd.DataFrame, list):
        self_like = WineQualityDataset()
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
        df, added = WineQualityDataset.expand_features_on_dataframe(df)
        try:
            df.attrs["agent_expansion_applied"] = True
            df.attrs["agent_provider"] = agent_provider
            df.attrs["agent_expanded_features"] = added
        except Exception:
            pass
        return df
