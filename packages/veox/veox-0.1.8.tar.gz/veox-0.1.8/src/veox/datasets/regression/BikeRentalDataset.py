import os
import pandas as pd
import numpy as np
import requests
import zipfile
from io import BytesIO
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class BikeRentalDataset(BaseDatasetLoader):
    """
    Loader for the Bike Sharing dataset from the UCI Machine Learning Repository.
    
    This dataset contains daily counts of rental bikes between 2011 and 2012 in the
    Capital bikeshare system in Washington DC, with corresponding weather and
    seasonal information. The task is to predict the daily count of bike rentals.
    
    Features include weather conditions, day of week, and other temporal information.
    Target is the count of total rental bikes ('cnt').
    """
    
    def get_dataset_info(self):
        """Dataset metadata for the loader framework"""
        return {
            'name': 'BikeRentalDataset',
            'source_id': 'uci:bike_sharing',  # Unique identifier
            'category': 'regression',
            'description': 'Bike Sharing Dataset: daily bike rental counts with weather and temporal features.'
        }
    
    def download_dataset(self, info):
        """Download and process the dataset from UCI repository"""
        dataset_name = info['name']
        data_file_in_zip = "day.csv"  # We'll use the daily aggregation file
        
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00275/Bike-Sharing-Dataset.zip"
        print(f"[{dataset_name}] Downloading from URL: {url}")
        
        try:
            r = requests.get(url, timeout=60)
            print(f"[{dataset_name}] HTTP response status: {r.status_code}")
            if r.status_code != 200:
                raise Exception(f"Failed to download dataset: HTTP {r.status_code}")
            
            # Process ZIP file
            with zipfile.ZipFile(BytesIO(r.content)) as z:
                print(f"[{dataset_name}] Extracting {data_file_in_zip} from ZIP...")
                
                # List files in the zip to find the correct path
                file_list = z.namelist()
                print(f"[{dataset_name}] Files in ZIP: {file_list}")
                
                # Find the day.csv file (it might be in a subdirectory)
                day_file_path = None
                for file_path in file_list:
                    if file_path.endswith(data_file_in_zip):
                        day_file_path = file_path
                        break
                
                if day_file_path is None:
                    raise Exception(f"{data_file_in_zip} not found in ZIP file")
                
                # Extract day.csv
                with z.open(day_file_path) as data_file:
                    content = data_file.read()
                    print(f"[{dataset_name}] Extracted {day_file_path}")
                    return content
            
        except Exception as e:
            print(f"[{dataset_name}] Download or processing failed: {str(e)}")
            raise
    
    def process_dataframe(self, df, info):
        """Process the dataset into final form"""
        dataset_name = info['name']
        
        print(f"[{dataset_name}] DataFrame shape: {df.shape}")
        print(f"[{dataset_name}] Data types of columns:\n{df.dtypes}")
        print(f"[{dataset_name}] First 5 rows:\n{df.head().to_string()}")
        
        # Column descriptions:
        # - instant: record index
        # - dteday : date
        # - season : season (1:winter, 2:spring, 3:summer, 4:fall)
        # - yr : year (0: 2011, 1:2012)
        # - mnth : month (1 to 12)
        # - holiday : weather day is holiday or not
        # - weekday : day of the week
        # - workingday : if day is neither weekend nor holiday is 1, otherwise is 0.
        # - weathersit : weather situation (1: Clear to 4: Heavy Rain/Snow) 
        # - temp : Normalized temperature in Celsius
        # - atemp: Normalized feeling temperature in Celsius
        # - hum: Normalized humidity
        # - windspeed: Normalized wind speed
        # - casual: count of casual users
        # - registered: count of registered users
        # - cnt: count of total rental bikes including both casual and registered
        
        # Set the count of total rentals as target if not already set
        if 'target' not in df.columns:
            df['target'] = df['cnt']
            print(f"[{dataset_name}] Set 'cnt' as the target column")
        
        # Drop non-numeric columns
        drop_cols = ['instant', 'dteday']
        for col in drop_cols:
            if col in df.columns:
                df = df.drop(col, axis=1)
                print(f"[{dataset_name}] Dropped '{col}' column")
        
        print(f"[{dataset_name}] Checking for missing values:")
        for col in df.columns:
            missing = df[col].isna().sum()
            print(f"  - {col}: {missing} missing")
        
        # Handle missing values if any
        if df.isna().any().any():
            print(f"[{dataset_name}] Filling missing values...")
            for col in df.columns:
                if df[col].isna().any():
                    if pd.api.types.is_numeric_dtype(df[col]):
                        df[col] = df[col].fillna(df[col].median())
                    else:
                        df[col] = df[col].fillna(df[col].mode()[0])
        
        print(f"[{dataset_name}] Shuffling the dataset randomly...")
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        print(f"[{dataset_name}] Dataset shuffled and indices reset.")
        
        print(f"[{dataset_name}] Final DataFrame shape: {df.shape}")
        print(f"[{dataset_name}] Target summary:")
        print(f"  - Mean: {df['target'].mean():.2f}")
        print(f"  - Std: {df['target'].std():.2f}")
        print(f"  - Min: {df['target'].min():.2f}")
        print(f"  - Max: {df['target'].max():.2f}")
        print(f"[{dataset_name}] Sample of first 5 rows:\n{df.head().to_string()}")
        
        # Attach lightweight attrs to help downstream expansion
        try:
            df.attrs["dataset_source"] = "BikeRentalDataset"
            df.attrs["raw_feature_names"] = [c for c in df.columns if c != 'target']
            df.attrs["feature_expander"] = ("BikeRentalDataset", "expand_features_on_dataframe")
        except Exception:
            pass
        
        return df

    # ------------------------------------------------------------------
    # Agent-aware feature engineering hooks (Bike Rental)
    # ------------------------------------------------------------------
    def get_feature_agent(self, provider: str = "GPT5"):
        return {"provider": provider, "name": "BikeRentalFeatureAgent", "version": "v1"}

    def _propose_agent_feature_plan(self, df: pd.DataFrame, agent) -> list:
        eps = 1e-6
        def has_all(cols):
            return all(c in df.columns for c in cols)

        plan = []

        # Temperature features
        if has_all(['temp', 'atemp']):
            plan.append({
                "name": "temp_diff",
                "requires": ["temp", "atemp"],
                "builder": lambda d: d["atemp"] - d["temp"],
            })
            plan.append({
                "name": "temp_squared",
                "requires": ["temp"],
                "builder": lambda d: d["temp"] ** 2,
            })
            plan.append({
                "name": "is_comfortable_temp",
                "requires": ["temp"],
                "builder": lambda d: ((d["temp"] > 0.3) & (d["temp"] < 0.7)).astype(float),
            })

        # Humidity features
        if has_all(['hum']):
            plan.append({
                "name": "is_dry",
                "requires": ["hum"],
                "builder": lambda d: (d["hum"] < 0.4).astype(float),
            })
            plan.append({
                "name": "is_humid",
                "requires": ["hum"],
                "builder": lambda d: (d["hum"] > 0.7).astype(float),
            })

        # Wind features
        if has_all(['windspeed']):
            plan.append({
                "name": "is_windy",
                "requires": ["windspeed"],
                "builder": lambda d: (d["windspeed"] > 0.3).astype(float),
            })

        # Weather condition features
        if has_all(['weathersit']):
            plan.append({
                "name": "is_clear",
                "requires": ["weathersit"],
                "builder": lambda d: (d["weathersit"] == 1).astype(float),
            })
            plan.append({
                "name": "is_bad_weather",
                "requires": ["weathersit"],
                "builder": lambda d: (d["weathersit"] >= 3).astype(float),
            })

        # Temporal features
        if has_all(['season']):
            plan.append({
                "name": "is_summer",
                "requires": ["season"],
                "builder": lambda d: (d["season"] == 3).astype(float),
            })

        if has_all(['mnth']):
            plan.append({
                "name": "month_sin",
                "requires": ["mnth"],
                "builder": lambda d: np.sin(2 * np.pi * d["mnth"] / 12),
            })
            plan.append({
                "name": "month_cos",
                "requires": ["mnth"],
                "builder": lambda d: np.cos(2 * np.pi * d["mnth"] / 12),
            })

        # Work/holiday interactions
        if has_all(['workingday', 'holiday']):
            plan.append({
                "name": "is_regular_workday",
                "requires": ["workingday", "holiday"],
                "builder": lambda d: ((d["workingday"] == 1) & (d["holiday"] == 0)).astype(float),
            })

        # Weather-temporal interactions
        if has_all(['temp', 'season']):
            plan.append({
                "name": "temp_season_interaction",
                "requires": ["temp", "season"],
                "builder": lambda d: d["temp"] * d["season"],
            })

        if has_all(['hum', 'windspeed']):
            plan.append({
                "name": "discomfort_index",
                "requires": ["hum", "windspeed"],
                "builder": lambda d: d["hum"] * d["windspeed"],
            })

        return plan

    @staticmethod
    def expand_features_on_dataframe(df: pd.DataFrame) -> (pd.DataFrame, list):
        self_like = BikeRentalDataset()
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
    dataset = BikeRentalDataset()
    df = dataset.get_data()
    print(f"Dataset loaded successfully with {len(df)} rows.")
    
    # Test expansion
    df_exp = dataset.get_data_gen()
    print(f"Expanded dataset has {len(df_exp.columns)} columns") 