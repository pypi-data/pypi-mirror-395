import os
import pandas as pd
import requests
import zipfile
from io import BytesIO
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class CombinedCyclePowerPlantDataset(BaseDatasetLoader):
    """
    Loader for the Combined Cycle Power Plant dataset from the UCI Machine Learning Repository.
    
    This dataset contains data collected from a Combined Cycle Power Plant over 6 years (2006-2011) 
    when the power plant was set to work with full load. Features consist of hourly average 
    ambient variables Temperature (T), Ambient Pressure (AP), Relative Humidity (RH) and 
    Exhaust Vacuum (V) to predict the net hourly electrical energy output (PE) of the plant.
    
    Features: Temperature, Ambient Pressure, Relative Humidity, Exhaust Vacuum
    Target: Net hourly electrical energy output
    """

    def get_dataset_info(self):
        """Dataset metadata for the loader framework"""
        return {
            'name': 'CombinedCyclePowerPlantDataset',
            'source_id': 'uci:ccpp',  # Unique identifier
            'category': 'regression',
            'description': 'Combined Cycle Power Plant dataset: regression to predict electrical energy output based on ambient variables.',
        }
    
    def download_dataset(self, info):
        """Download dataset from UCI repository and process Excel file"""
        dataset_name = info['name']
        excel_file_in_zip = "CCPP/Folds5x2_pp.xlsx"  # Path to the Excel file within the ZIP
        
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00294/CCPP.zip"
        print(f"[{dataset_name}] Downloading from URL: {url}")
        
        try:
            r = requests.get(url, timeout=60)  # Increased timeout for larger file
            print(f"[{dataset_name}] HTTP response status: {r.status_code}")
            if r.status_code != 200:
                raise Exception(f"Failed to download dataset: HTTP {r.status_code}")
            
            # Process ZIP file to extract Excel data
            with zipfile.ZipFile(BytesIO(r.content)) as z:
                print(f"[{dataset_name}] Extracting {excel_file_in_zip} from ZIP...")
                
                # Read Excel file from zip
                xls_file_bytes = z.read(excel_file_in_zip)
                xls = pd.ExcelFile(BytesIO(xls_file_bytes))
                
                # Concatenate all sheets
                df_from_excel = pd.DataFrame()
                for sn in xls.sheet_names:
                    sheet_df = xls.parse(sn)
                    df_from_excel = pd.concat([df_from_excel, sheet_df], ignore_index=True)
                
                if df_from_excel.empty:
                    raise Exception("No data extracted from Excel file.")
                
                # Convert DataFrame to CSV
                csv_buffer = BytesIO()
                df_from_excel.to_csv(csv_buffer, index=False)
                csv_data = csv_buffer.getvalue()
                
                print(f"[{dataset_name}] Successfully converted Excel to CSV, size: {len(csv_data)} bytes")
                
                # Sanity check on size
                if len(csv_data) < 100000:  # Adjusted sanity check size
                    print(f"[{dataset_name}] CSV data too small: {len(csv_data)} bytes. Expected >100 KB.")
                    print(f"[{dataset_name}] Shape of DataFrame from Excel: {df_from_excel.shape}")
                    raise Exception(f"Processed data too small: {len(csv_data)} bytes.")
                
                return csv_data
        except Exception as e:
            print(f"[{dataset_name}] Download or processing failed: {str(e)}")
            raise
    
    def process_dataframe(self, df, info):
        """Process the dataset into final form"""
        dataset_name = info['name']
        
        print(f"[{dataset_name}] DataFrame shape: {df.shape}")
        print(f"[{dataset_name}] Data types of columns:\n{df.dtypes}")
        print(f"[{dataset_name}] First 5 rows:\n{df.head().to_string()}")
        
        # Set PE as target if not already set
        if 'PE' in df.columns and 'target' not in df.columns:
            df['target'] = df['PE']
            print(f"[{dataset_name}] Set 'PE' as the target column")
        
        print(f"[{dataset_name}] Checking for missing values:")
        for col in df.columns:
            missing = df[col].isna().sum()
            print(f"  - {col}: {missing} missing")
        
        # This dataset is typically clean, but good to have the check
        if df.isna().any().any():
            print(f"[{dataset_name}] Filling missing values with column medians...")
            for col in df.columns:
                if df[col].isna().any():
                    if pd.api.types.is_numeric_dtype(df[col]):
                        df[col] = df[col].fillna(df[col].median())
        
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
        
        return df

# For testing
if __name__ == "__main__":
    dataset = CombinedCyclePowerPlantDataset()
    df = dataset.get_data()
    print(f"Dataset loaded successfully with {len(df)} rows.") 