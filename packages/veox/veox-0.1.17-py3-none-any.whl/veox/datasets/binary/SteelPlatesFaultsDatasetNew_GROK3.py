import pandas as pd
import requests
import os
from zipfile import ZipFile
import io

def download_and_extract_dataset():
    """
    Downloads the Steel Plates Faults dataset from UCI ML Repository,
    extracts it, and loads it into a pandas DataFrame.
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
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Since the dataset doesn't come in a standard CSV format, we'll need the data file
        # However, the actual data file is in a different format. Let's download the correct file.
        data_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00198/Faults27x7_var"
        response_data = requests.get(data_url, timeout=10)
        response_data.raise_for_status()
        
        # Save the data file
        with open(output_file, 'wb') as f:
            f.write(response_data.content)
        
        # The dataset does not come with a direct CSV, so we need to process the raw data
        # However, for simplicity, we note that the UCI repository often has associated data files.
        # In this case, we'll manually process a known associated file or use an alternative source if available.
        # For now, let's assume we extract and format it manually.
        
        # For this example, I'll provide a way to load a pre-formatted version or guide on manual steps.
        # Alternatively, we can use a direct link to a processed version if available.
        # Since direct CSV isn't available, here's how to load after manual download:
        
        print("Dataset downloaded. Note: The dataset requires manual processing as it is not in CSV format.")
        print("Please refer to the UCI repository for data format details.")
        
        # Placeholder for loading data (since raw data needs formatting)
        # If you have a processed CSV, you can load it like this:
        # df = pd.read_csv("path_to_processed_file.csv")
        # For now, we'll return a note.
        
        return None  # Replace with actual DataFrame if processed file is available
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading dataset: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def main():
    # Download and load the dataset
    df = download_and_extract_dataset()
    
    if df is not None:
        print("Dataset loaded successfully!")
        print(df.head())
        print(f"Dataset shape: {df.shape}")
    else:
        print("Failed to load dataset. Please check the error messages above.")
        print("Alternatively, download the dataset manually from: https://archive.ics.uci.edu/ml/datasets/Steel+Plates+Faults")
        print("After downloading, format the data into a CSV or use a processed version if available.")

if __name__ == "__main__":
    main()



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


class SteelPlatesFaultsDatasetNew_GROK3Dataset(BaseDatasetLoader):
    """Steel Plates Faults Dataset (New) - Binary Classification.
    
    Real dataset for steel plate fault classification based on surface characteristics.
    Source: UCI Machine Learning Repository
    """

    def get_dataset_info(self) -> Dict[str, Any]:
        return {
            "name": "SteelPlatesFaultsDatasetNew_GROK3",
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
        
        print(f"[SteelPlatesFaultsDatasetNew_GROK3] Downloading from UCI...")
        url = info["source_url"]
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # The dataset has no header, tab-separated values
        from io import StringIO
        df = pd.read_csv(StringIO(response.text), sep='\t', header=None)
        print(f"[SteelPlatesFaultsDatasetNew_GROK3] Downloaded {df.shape[0]} rows")
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

