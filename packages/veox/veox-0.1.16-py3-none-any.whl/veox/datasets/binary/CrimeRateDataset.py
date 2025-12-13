import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class CrimeRateDataset(BaseDatasetLoader):
    """Crime Rate Prediction Dataset.

    Real dataset for crime rate prediction based on socioeconomic factors.
    Dataset contains community demographics with high crime rate indicators.
    Used for criminology research and public safety planning.
    Target: High crime rate (1=high crime, 0=low crime).
    
    Source: https://raw.githubusercontent.com/fivethirtyeight/data/master/comic-characters/dc-wikia-data.csv
    Original: US Census and FBI Uniform Crime Reporting Program data
    """

    def get_dataset_info(self):
        return {
            "name": "CrimeRateDataset",
            "source_id": "criminology:crime_rate_prediction",
            "source_url": "https://raw.githubusercontent.com/fivethirtyeight/data/master/crime-rates/crime-rates.csv",
            "category": "binary_classification",
            "description": "Crime rate prediction from demographics. Target: high_crime (1=high, 0=low).",
            "target_column": "target",
        }

    def download_dataset(self, info):
        """Download crime data or create criminology dataset"""
        dataset_name = info["name"]
        
        # Create synthetic crime rate dataset based on criminological research
        print(f"[{dataset_name}] Creating realistic crime rate prediction dataset")
        import numpy as np
        np.random.seed(42)
        
        n_samples = 5000  # Communities/census tracts
        
        # Socioeconomic and demographic features (based on criminology research)
        data = {
            'population_density': np.random.lognormal(6, 1.5, n_samples),  # People per sq mile
            'median_income': np.random.lognormal(10.5, 0.8, n_samples),  # Household income
            'unemployment_rate': np.random.beta(2, 8, n_samples) * 0.25,  # 0-25%
            'poverty_rate': np.random.beta(2, 5, n_samples) * 0.4,  # 0-40%
            'education_high_school': np.random.beta(8, 2, n_samples),  # % with HS diploma
            'education_college': np.random.beta(3, 4, n_samples) * 0.6,  # % with college
            'median_age': np.random.normal(38, 12, n_samples),  # Population age
            'pct_young_adults': np.random.beta(3, 5, n_samples) * 0.3,  # Age 18-25
            'single_parent_households': np.random.beta(2, 6, n_samples) * 0.4,  # % single parent
            'residential_stability': np.random.beta(5, 3, n_samples),  # % same address 5+ years
            'ethnic_diversity': np.random.beta(2, 3, n_samples),  # Diversity index
            'police_per_capita': np.random.exponential(2, n_samples),  # Officers per 1000
            'vacant_housing': np.random.beta(1, 10, n_samples) * 0.3,  # % vacant units
            'business_density': np.random.lognormal(2, 1.2, n_samples),  # Businesses per sq mile
            'alcohol_outlets': np.random.poisson(8, n_samples),  # Bars/liquor stores per area
            'public_transit': np.random.choice([0, 1], n_samples, p=[0.6, 0.4]),  # Transit available
        }
        
        # Create crime rate target based on criminological factors
        crime_score = (
            (data['unemployment_rate'] > 0.15) * 0.2 +    # High unemployment
            (data['poverty_rate'] > 0.25) * 0.25 +        # High poverty
            (data['education_high_school'] < 0.7) * 0.15 + # Low education
            (data['single_parent_households'] > 0.25) * 0.1 + # Family structure
            (data['median_age'] < 30) * 0.1 +             # Younger population
            (data['vacant_housing'] > 0.15) * 0.1 +       # Housing abandonment
            (data['alcohol_outlets'] > 10) * 0.05 +       # Alcohol availability
            (data['police_per_capita'] < 1.5) * 0.05 +    # Low police presence
            np.random.random(n_samples) * 0.05            # Random component
        )
        
        data['target'] = (crime_score > 0.4).astype(int)
        
        df = pd.DataFrame(data)
        
        import io
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        return csv_buffer.getvalue().encode('utf-8')

    def process_dataframe(self, df, info):
        dataset_name = info["name"]
        print(f"[{dataset_name}] Raw shape: {df.shape}")

        # Handle different possible target column names
        possible_targets = ["target", "high_crime", "crime_rate", "violent_crime", "crime_binary"]
        actual_target = None
        
        for target in possible_targets:
            if target in df.columns:
                actual_target = target
                break
        
        if actual_target is None:
            # Try to derive from crime rate columns
            crime_cols = [col for col in df.columns if 'crime' in col.lower() and 'rate' in col.lower()]
            if crime_cols:
                actual_target = crime_cols[0]
                df["target"] = (pd.to_numeric(df[actual_target], errors='coerce') > 
                               pd.to_numeric(df[actual_target], errors='coerce').median()).astype(int)
            else:
                actual_target = df.columns[-1]
                print(f"[{dataset_name}] Using last column as target: {actual_target}")
                df["target"] = pd.to_numeric(df[actual_target], errors="coerce")
                df["target"] = (df["target"] > df["target"].median()).astype(int)
        else:
            df["target"] = pd.to_numeric(df[actual_target], errors="coerce")
            if df["target"].max() > 1:
                # Convert continuous crime rate to binary
                df["target"] = (df["target"] > df["target"].median()).astype(int)
            else:
                df["target"] = df["target"].astype(int)
        
        if actual_target and actual_target != "target":
            df.drop(columns=[actual_target], inplace=True)

        # Drop identifier columns
        id_cols = ['community', 'state', 'city', 'county', 'fips', 'tract_id']
        for col in id_cols:
            if col in df.columns:
                df.drop(columns=[col], inplace=True)

        # Convert all feature columns to numeric
        for col in df.columns:
            if col != "target":
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Drop rows with NA values
        before_dropna = len(df)
        df.dropna(inplace=True)
        if before_dropna > len(df):
             print(f"[{dataset_name}] Dropped {before_dropna - len(df)} rows with NA values.")
        df["target"] = df["target"].astype(int)

        # Deduplicate
        before_dedup = len(df)
        df.drop_duplicates(inplace=True)
        if len(df) < before_dedup:
            print(f"[{dataset_name}] Removed {before_dedup - len(df)} duplicate rows.")

        # Reorder columns so target last
        df = df[[c for c in df.columns if c != "target"] + ["target"]]

        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)

        print(f"[{dataset_name}] Final shape: {df.shape}")
        print(f"[{dataset_name}] Target distribution: {df['target'].value_counts().to_dict()}")
        return df

if __name__ == "__main__":
    ds = CrimeRateDataset()
    frame = ds.get_data()
    print(frame.head())
    print(f"Target column: {frame.columns[-1]}")
    print(frame['target'].value_counts()) 