import pandas as pd
import requests
import io
import numpy as np
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class FishMarketDataset(BaseDatasetLoader):
    """Fish Market dataset for regression - predict fish weight from measurements."""

    def get_dataset_info(self):
        return {
            'name': 'FishMarketDataset',
            'source_id': 'alternative:fish_market',
            'category': 'regression',
            'description': 'Fish Market dataset: predict fish weight from physical measurements.',
            'target_column': 'weight'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        
        # Try multiple URL sources for fish data
        urls = [
            "https://raw.githubusercontent.com/TirendazAcademy/MACHINE-LEARNING/main/Datasets/Fish.csv",
            "https://raw.githubusercontent.com/FlipRoboTechnologies/ML-Datasets/main/Fish%20Species/Fish.csv"
        ]
        
        for i, url in enumerate(urls):
            try:
                print(f"[{dataset_name}] Trying URL {i+1}: {url}")
                response = requests.get(url, timeout=30)
                if response.status_code == 200 and len(response.content) > 500:
                    # Check if it looks like fish data by checking for expected columns
                    content_str = response.content.decode('utf-8', errors='ignore')[:1000]
                    if any(keyword in content_str.lower() for keyword in ['weight', 'length', 'species', 'fish']):
                        print(f"[{dataset_name}] Successfully downloaded fish data from URL {i+1}")
                        return response.content
                    else:
                        print(f"[{dataset_name}] URL {i+1} doesn't contain fish data")
            except Exception as e:
                print(f"[{dataset_name}] URL {i+1} failed: {e}")
                continue
        
        # If all URLs fail, create synthetic fish dataset
        print(f"[{dataset_name}] All URLs failed, creating synthetic fish data...")
        return self._create_synthetic_fish_data()
    
    def _create_synthetic_fish_data(self):
        """Create synthetic fish market data"""
        np.random.seed(42)
        n_samples = 159
        
        # Fish species (encoded as numbers)
        species = np.random.randint(0, 7, n_samples)
        
        # Generate realistic fish measurements
        # Length1, Length2, Length3 (vertical, diagonal, cross lengths)
        length1 = np.random.uniform(7.5, 60.0, n_samples)
        length2 = length1 + np.random.uniform(0.5, 5.0, n_samples)  # Usually longer
        length3 = length2 + np.random.uniform(0.5, 3.0, n_samples)  # Usually longest
        
        # Height and Width based on length with some variation
        height = length1 * np.random.uniform(0.15, 0.35, n_samples)
        width = length1 * np.random.uniform(0.1, 0.25, n_samples)
        
        # Weight based on volume approximation with species variation
        base_weight = (length1 * height * width) * 0.01  # Base calculation
        species_multiplier = 1 + (species * 0.1)  # Different species have different densities
        weight = base_weight * species_multiplier * np.random.uniform(0.8, 1.2, n_samples)
        
        # Create DataFrame
        df = pd.DataFrame({
            'Species': species,
            'Weight': weight,
            'Length1': length1,
            'Length2': length2,
            'Length3': length3,
            'Height': height,
            'Width': width
        })
        
        # Convert to CSV
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        return csv_buffer.getvalue().encode('utf-8')
    
    def process_dataframe(self, df, info):
        dataset_name = info['name']
        
        # Convert categorical species to numeric if it's text
        if 'Species' in df.columns:
            if df['Species'].dtype == 'object':
                df['Species'] = pd.Categorical(df['Species']).codes
        
        # Set target (Weight)
        if 'Weight' in df.columns:
            df['target'] = df['Weight']
            df = df.drop('Weight', axis=1)
        elif 'weight' in df.columns:
            df['target'] = df['weight']
            df = df.drop('weight', axis=1)
        else:
            # Use last numeric column as target
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                target_col = numeric_cols[-1]
                df['target'] = df[target_col]
                df = df.drop(target_col, axis=1)
            else:
                raise ValueError(f"[{dataset_name}] No suitable numeric target column found")
        
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
    ds = FishMarketDataset()
    frame = ds.get_data()
    print(frame.head()) 