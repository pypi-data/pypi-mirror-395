import pandas as pd
import requests
import os
from zipfile import ZipFile
import io

def download_and_extract_dataset():
    """
    Downloads and extracts the Steel Plates Faults dataset from UCI ML Repository.
    Returns the dataset as a pandas DataFrame.
    """
    try:
        # URL for the dataset
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00198/Faults27x7_var"
        output_dir = "steel_plates_faults_data"
        output_file = os.path.join(output_dir, "Faults.Names")
        
        # Create directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Download the dataset
        print("Downloading dataset...")
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(output_file, 'wb') as f:
                f.write(response.content)
            print(f"Dataset downloaded and saved to {output_file}")
        else:
            raise Exception(f"Failed to download dataset. Status code: {response.status_code}")
            
        # Since the actual data is in a different file, we need to download the data file as well
        data_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00198/Faults27x7_var"
        data_file = os.path.join(output_dir, "Faults27x7_var")
        
        # The dataset doesn't have a direct CSV, so we'll use the provided data
        # However, the UCI repository page mentions the data is in the .data file
        # After checking, I found the correct data file name
        correct_data_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00198/Faults27x7_var"
        print("Note: The actual data needs manual processing. For simplicity, we'll use a processed version.")
        
        # Load a processed version of the dataset (since raw data needs attribute names mapping)
        # Alternatively, provide a direct link to processed data if available or process it manually
        # For simplicity, I'll assume we process it into a CSV format manually
        # However, to make this code executable, I'll provide a way to load sample data
        
        # Correct URL for data file
        correct_data_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00198/Faults27x7_var"
        response = requests.get(correct_data_url)
        if response.status_code == 200:
            # Save the raw data
            with open(data_file, 'wb') as f:
                f.write(response.content)
            print(f"Raw data downloaded to {data_file}")
            
            # Process the data into a DataFrame (based on dataset description)
            # The dataset has 27 attributes + 7 binary fault indicators
            # We'll create a binary classification problem by combining fault indicators
            column_names = [
                'X_Minimum', 'X_Maximum', 'Y_Minimum', 'Y_Maximum', 'Pixels_Areas', 
                'X_Perimeter', 'Y_Perimeter', 'Sum_of_Luminosity', 'Minimum_of_Luminosity', 
                'Maximum_of_Luminosity', 'Length_of_Conveyer', 'TypeOfSteel_A300', 
                'TypeOfSteel_A400', 'Steel_Plate_Thickness', 'Edges_Index', 'Empty_Index', 
                'Square_Index', 'Outside_X_Index', 'Edges_X_Index', 'Edges_Y_Index', 
                'Outside_Global_Index', 'LogOfAreas', 'Log_X_Index', 'Log_Y_Index', 
                'Orientation_Index', 'Luminosity_Index', 'SigmoidOfAreas',
                'Pastry', 'Z_Scratch', 'K_Scratch', 'Stains', 'Dirtiness', 'Bumps', 'Other_Faults'
            ]
            
            # Read the data (space-separated, no header in original file)
            df = pd.read_csv(data_file, sep=r'\s+', header=None, names=column_names)
            print("Dataset loaded into DataFrame.")
            
            # Create a binary classification target (1 if any fault, 0 if no fault)
            fault_columns = ['Pastry', 'Z_Scratch', 'K_Scratch', 'Stains', 'Dirtiness', 'Bumps', 'Other_Faults']
            df['Fault'] = df[fault_columns].max(axis=1)
            df.drop(columns=fault_columns, inplace=True)
            
            # Save the processed dataset as CSV for future use
            processed_file = os.path.join(output_dir, "steel_plates_faults_processed.csv")
            df.to_csv(processed_file, index=False)
            print(f"Processed dataset saved to {processed_file}")
            
            return df
        else:
            raise Exception(f"Failed to download data file. Status code: {response.status_code}")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    # Download and load the dataset
    df = download_and_extract_dataset()
    if df is not None:
        print("\nDataset Preview (first 5 rows):")
        print(df.head())
        print("\nDataset Shape:", df.shape)
        print("\nClass Distribution:")
        print(df['Fault'].value_counts())



from typing import Dict, Any
import pandas as pd
try:
    from app.datasets.BaseDatasetLoader import BaseDatasetLoader
except Exception:  # pragma: no cover
    class BaseDatasetLoader:  # type: ignore
        def get_dataset_info(self) -> Dict[str, Any]:
            raise NotImplementedError
        def download_dataset(self, info: Dict[str, Any]):
            raise NotImplementedError
        def process_dataframe(self, df: pd.DataFrame, info: Dict[str, Any]) -> pd.DataFrame:
            return df


class SteelPlatesFaultsDataset_GROK3Dataset(BaseDatasetLoader):
    """Steel Plates Faults Dataset - Binary Classification.
    
    Real dataset for steel plate fault classification based on surface characteristics.
    Source: UCI Machine Learning Repository
    """

    def get_dataset_info(self) -> Dict[str, Any]:
        return {
            "name": "SteelPlatesFaultsDataset_GROK3",
            "source_id": "uci:steel_plates_faults",
            "source_url": "https://archive.ics.uci.edu/ml/machine-learning-databases/00198/Faults.NNA",
            "category": "binary_classification",
            "description": "Steel plates fault detection. Target: fault_detected (1=fault, 0=no fault).",
            "target_column": "Pastry",
        }

    def download_dataset(self, info: Dict[str, Any]):
        """Download the Steel Plates Faults dataset from UCI"""
        import requests
        from io import StringIO
        
        print(f"[SteelPlatesFaultsDataset_GROK3] Downloading from UCI...")
        url = info["source_url"]
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # The dataset has no header, tab-separated values
        from io import StringIO
        df = pd.read_csv(StringIO(response.text), sep='\t', header=None)
        print(f"[SteelPlatesFaultsDataset_GROK3] Downloaded {df.shape[0]} rows")
        return df.to_csv(index=False).encode('utf-8')

    def process_dataframe(self, df: pd.DataFrame, info: Dict[str, Any]) -> pd.DataFrame:
        """Process steel plates faults dataset"""
        dataset_name = info["name"]
        print(f"[{dataset_name}] Raw shape: {df.shape}")

        # The Steel Plates dataset has specific columns for fault types
        expected_fault_cols = ['Pastry', 'Z_Scratch', 'K_Scatch', 'Stains', 'Dirtiness', 'Bumps', 'Other_Faults']
        
        # Assign column names if needed
        if df.shape[1] == 34:  # 27 features + 7 fault types
            feature_cols = [
                'X_Minimum', 'X_Maximum', 'Y_Minimum', 'Y_Maximum', 'Pixels_Areas', 
                'X_Perimeter', 'Y_Perimeter', 'Sum_of_Luminosity', 'Minimum_of_Luminosity', 
                'Maximum_of_Luminosity', 'Length_of_Conveyer', 'TypeOfSteel_A300', 
                'TypeOfSteel_A400', 'Steel_Plate_Thickness', 'Edges_Index', 'Empty_Index', 
                'Square_Index', 'Outside_X_Index', 'Edges_X_Index', 'Edges_Y_Index', 
                'Outside_Global_Index', 'LogOfAreas', 'Log_X_Index', 'Log_Y_Index', 
                'Orientation_Index', 'Luminosity_Index', 'SigmoidOfAreas'
            ] + expected_fault_cols
            df.columns = feature_cols
        
        # Create binary target: 1 if any fault is present, 0 if no faults
        fault_present = False
        for fault_col in expected_fault_cols:
            if fault_col in df.columns:
                if not fault_present:
                    df['any_fault'] = pd.to_numeric(df[fault_col], errors='coerce')
                    fault_present = True
                else:
                    df['any_fault'] = df['any_fault'] | pd.to_numeric(df[fault_col], errors='coerce')
        
        if fault_present:
            df["target"] = df['any_fault'].fillna(0).astype(int)
            df.drop(columns=['any_fault'], inplace=True)
            # Drop individual fault columns after creating binary target
            for fault_col in expected_fault_cols:
                if fault_col in df.columns:
                    df.drop(columns=[fault_col], inplace=True)
        else:
            raise ValueError(f"[{dataset_name}] Could not find fault columns")
        
        # Ensure all features are numeric
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

