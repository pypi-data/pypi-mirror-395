import os
import pandas as pd
import requests
import io
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class ConcreteStrengthDataset(BaseDatasetLoader):
    """
    Loader for the Concrete Compressive Strength dataset from the UCI Machine Learning Repository.
    
    This dataset contains information about concrete mixtures and their resulting compressive strength.
    The task is to predict the compressive strength based on the components and age of the mixture.
    
    Features include cement quantity, blast furnace slag, fly ash, water, superplasticizer, and more.
    Target is the compressive strength in megapascals (MPa).
    """

    def get_dataset_info(self):
        """Dataset metadata for the loader framework"""
        return {
            'name': 'ConcreteStrengthDataset',
            'source_id': 'uci:concrete_strength',  # Unique identifier
            'category': 'regression',
            'description': 'Concrete Compressive Strength dataset: regression to predict strength based on mixture components.',
        }
    
    def download_dataset(self, info):
        """Download dataset from UCI repository and process Excel file"""
        dataset_name = info['name']
        
        # URL for the Concrete Strength dataset
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/concrete/compressive/Concrete_Data.xls"
        print(f"[{dataset_name}] Downloading from URL: {url}")
        
        try:
            r = requests.get(url, timeout=30)
            print(f"[{dataset_name}] HTTP response status: {r.status_code}")
            if r.status_code != 200:
                raise Exception(f"Failed to download dataset: HTTP {r.status_code}")
            
            # Convert XLS to CSV in memory
            try:
                # Read Excel into DataFrame
                xls_df = pd.read_excel(io.BytesIO(r.content))
                
                # Convert to CSV
                csv_buffer = io.BytesIO()
                xls_df.to_csv(csv_buffer, index=False)
                csv_data = csv_buffer.getvalue()
                
                print(f"[{dataset_name}] Successfully converted XLS to CSV, size: {len(csv_data)} bytes")
                
                if len(csv_data) < 5000:  # Sanity check for file size
                    print(f"[{dataset_name}] CSV data too small: {len(csv_data)} bytes. Expected >5 KB.")
                    raise Exception(f"Converted data too small: {len(csv_data)} bytes. Expected >5 KB.")
                
                return csv_data
            except Exception as e:
                print(f"[{dataset_name}] Failed to convert XLS to CSV: {str(e)}")
                raise
        except Exception as e:
            print(f"[{dataset_name}] Download or conversion failed: {str(e)}")
            raise
    
    def process_dataframe(self, df, info):
        """Process the dataset into final form"""
        dataset_name = info['name']
        
        # Rename columns to be more descriptive if needed
        column_map = {
            'Cement (component 1)(kg in a m^3 mixture)': 'cement',
            'Blast Furnace Slag (component 2)(kg in a m^3 mixture)': 'blast_furnace_slag',
            'Fly Ash (component 3)(kg in a m^3 mixture)': 'fly_ash',
            'Water (component 4)(kg in a m^3 mixture)': 'water',
            'Superplasticizer (component 5)(kg in a m^3 mixture)': 'superplasticizer',
            'Coarse Aggregate (component 6)(kg in a m^3 mixture)': 'coarse_aggregate',
            'Fine Aggregate (component 7)(kg in a m^3 mixture)': 'fine_aggregate',
            'Age (day)': 'age',
            'Concrete compressive strength(MPa, megapascals) ': 'compressive_strength'
        }
        
        # Check if columns need renaming
        if any(col in df.columns for col in column_map.keys()):
            df = df.rename(columns=column_map)
            print(f"[{dataset_name}] Renamed columns to more readable format")
        
        print(f"[{dataset_name}] DataFrame shape: {df.shape}")
        print(f"[{dataset_name}] Data types of columns:\n{df.dtypes}")
        print(f"[{dataset_name}] First 5 rows:\n{df.head().to_string()}")
        
        # Set the compressive_strength column as the 'target' for regression if not already set
        if 'compressive_strength' in df.columns and 'target' not in df.columns:
            df['target'] = df['compressive_strength']
            print(f"[{dataset_name}] Set 'compressive_strength' as the target column")
        
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
    dataset = ConcreteStrengthDataset()
    df = dataset.get_data()
    print(f"Dataset loaded successfully with {len(df)} rows.") 
    # ------------------------------------------------------------------
    # Agent-aware feature engineering hooks (Concrete Strength)
    # ------------------------------------------------------------------
    def get_feature_agent(self, provider: str = "GPT5"):
        return {"provider": provider, "name": "ConcreteStrengthFeatureAgent", "version": "v1"}

    def _propose_agent_feature_plan(self, df: pd.DataFrame, agent) -> list:
        import numpy as np
        eps = 1e-6
        def has_all(cols):
            return all(c in df.columns for c in cols)
        plan = []

        # Water-cement ratio (critical for concrete strength)
        if has_all(["water", "cement"]):
            plan.append({"name": "water_cement_ratio", "requires": ["water", "cement"],
                        "builder": lambda d: d["water"] / (d["cement"] + eps)})
        
        # Total binder content
        if has_all(["cement", "fly_ash", "blast_furnace_slag"]):
            plan.append({"name": "total_binder", "requires": ["cement", "fly_ash", "blast_furnace_slag"],
                        "builder": lambda d: d["cement"] + d["fly_ash"] + d["blast_furnace_slag"]})
            
            # Supplementary cementitious materials ratio
            plan.append({"name": "scm_ratio", "requires": ["cement", "fly_ash", "blast_furnace_slag"],
                        "builder": lambda d: (d["fly_ash"] + d["blast_furnace_slag"]) / (d["cement"] + d["fly_ash"] + d["blast_furnace_slag"] + eps)})
        
        # Water-binder ratio
        if has_all(["water", "cement", "fly_ash", "blast_furnace_slag"]):
            plan.append({"name": "water_binder_ratio", "requires": ["water", "cement", "fly_ash", "blast_furnace_slag"],
                        "builder": lambda d: d["water"] / (d["cement"] + d["fly_ash"] + d["blast_furnace_slag"] + eps)})
        
        # Aggregate ratios
        if has_all(["coarse_aggregate", "fine_aggregate"]):
            plan.append({"name": "aggregate_ratio", "requires": ["coarse_aggregate", "fine_aggregate"],
                        "builder": lambda d: d["coarse_aggregate"] / (d["fine_aggregate"] + eps)})
            plan.append({"name": "total_aggregate", "requires": ["coarse_aggregate", "fine_aggregate"],
                        "builder": lambda d: d["coarse_aggregate"] + d["fine_aggregate"]})
        
        # Paste volume features
        if has_all(["water", "cement", "fly_ash", "blast_furnace_slag", "superplasticizer"]):
            plan.append({"name": "paste_volume", "requires": ["water", "cement", "fly_ash", "blast_furnace_slag", "superplasticizer"],
                        "builder": lambda d: d["water"] + d["cement"]/3.15 + d["fly_ash"]/2.2 + d["blast_furnace_slag"]/2.9 + d["superplasticizer"]/1.2})
        
        # Age features
        if "age" in df.columns:
            plan.append({"name": "age_log", "requires": ["age"],
                        "builder": lambda d: np.log1p(d["age"])})
            plan.append({"name": "age_sqrt", "requires": ["age"],
                        "builder": lambda d: np.sqrt(d["age"])})
            plan.append({"name": "is_early_age", "requires": ["age"],
                        "builder": lambda d: (d["age"] <= 7).astype(int)})
            plan.append({"name": "is_mature", "requires": ["age"],
                        "builder": lambda d: (d["age"] >= 28).astype(int)})
        
        # Cement efficiency features
        if has_all(["cement", "age"]):
            plan.append({"name": "cement_age_interaction", "requires": ["cement", "age"],
                        "builder": lambda d: d["cement"] * np.log1p(d["age"])})
        
        # Superplasticizer effectiveness
        if has_all(["superplasticizer", "water"]):
            plan.append({"name": "sp_water_ratio", "requires": ["superplasticizer", "water"],
                        "builder": lambda d: d["superplasticizer"] / (d["water"] + eps)})
        
        if has_all(["superplasticizer", "cement"]):
            plan.append({"name": "sp_cement_ratio", "requires": ["superplasticizer", "cement"],
                        "builder": lambda d: d["superplasticizer"] / (d["cement"] + eps)})
        
        # Fineness modulus proxy
        if has_all(["fine_aggregate", "coarse_aggregate", "cement"]):
            plan.append({"name": "fineness_proxy", "requires": ["fine_aggregate", "coarse_aggregate", "cement"],
                        "builder": lambda d: (d["fine_aggregate"] + 0.1 * d["cement"]) / (d["coarse_aggregate"] + d["fine_aggregate"] + eps)})
        
        return plan

    @staticmethod
    def expand_features_on_dataframe(df: pd.DataFrame) -> (pd.DataFrame, list):
        self_like = ConcreteStrengthDataset()
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
        df, added = ConcreteStrengthDataset.expand_features_on_dataframe(df)
        try:
            df.attrs["agent_expansion_applied"] = True
            df.attrs["agent_provider"] = agent_provider
            df.attrs["agent_expanded_features"] = added
        except Exception:
            pass
        return df
