import os
import pandas as pd
import requests
import io
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class MushroomDataset(BaseDatasetLoader):
    """
    Loader for the UCI Mushroom dataset (binary classification: poisonous vs. edible).

    The original dataset has 8,124 rows and 23 columns:
      * The first column (class) is 'e' (edible) or 'p' (poisonous).
      * The remaining 22 columns describe various categorical features
        (cap shape, odor, gill size, stalk color, etc.).
      * Some rows have a '?' indicating missing or unknown data
        (e.g., 'stalk-root').
    
    Features include physical characteristics of the mushrooms (cap shape, odor, etc.).
    Target: Binary (0: edible, 1: poisonous)
    """

    def get_dataset_info(self):
        """Dataset metadata for the loader framework"""
        return {
            'name': 'MushroomDataset',
            'source_id': 'uci:mushroom',  # Unique identifier
            'category': 'binary_classification',
            'description': 'Mushroom dataset: binary classification to determine if mushrooms are edible or poisonous.',
        }
    
    def download_dataset(self, info):
        """Download dataset from UCI repository"""
        dataset_name = info['name']
        # UCI Mushroom Dataset link (agaricus-lepiota.data)
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/mushroom/agaricus-lepiota.data"
        print(f"[{dataset_name}] Downloading from URL: {url}")
        
        try:
            r = requests.get(url, timeout=30)
            print(f"[{dataset_name}] HTTP response status: {r.status_code}")
            if r.status_code != 200:
                raise Exception(f"Failed to download dataset: HTTP {r.status_code}")
            
            file_size = len(r.content)
            print(f"[{dataset_name}] Download complete. File size: {file_size} bytes")
            
            # Validate file size (expecting ~550 KB).
            if file_size < 100000:  # 100 KB as a simple threshold
                first_lines = r.content.decode("utf-8", errors="replace").splitlines()[:5]
                print(f"[{dataset_name}] File too small. First few lines:\n{os.linesep.join(first_lines)}")
                raise Exception(f"Downloaded file too small: {file_size} bytes. Expected >100 KB.")
                
            return r.content
        except Exception as exc:
            print(f"[{dataset_name}] Download failed: {exc}")
            raise
    
    def process_dataframe(self, df, info):
        """Process the dataset into final form"""
        dataset_name = info['name']
        
        # The mushroom dataset has a specific format where columns don't have names
        # and first column is the class: 'p' for poisonous or 'e' for edible
        print(f"[{dataset_name}] Initial DataFrame shape: {df.shape}")
        print(f"[{dataset_name}] Initial column names: {df.columns.tolist()}")
        
        # For agaricus-lepiota.data format, we may need to manually parse
        if df.shape[1] == 1:
            # Data might be loaded as a single column with comma-separated values
            print(f"[{dataset_name}] Data loaded as a single column, attempting to split")
            
            # Check if first row has commas - if so, we need to split
            first_row = df.iloc[0, 0]
            if isinstance(first_row, str) and ',' in first_row:
                # Split the text in the first column by commas
                rows = []
                for _, row in df.iterrows():
                    values = row[0].split(',')
                    rows.append(values)
                
                # Create a new DataFrame with the split data
                df = pd.DataFrame(rows)
                print(f"[{dataset_name}] Successfully split comma-delimited data into {df.shape[1]} columns")
        
        # If loaded without column names, assign them
        if all(isinstance(col, int) for col in df.columns):
            columns = [
                "class",  # 'p' = poisonous, 'e' = edible
                "cap_shape",
                "cap_surface",
                "cap_color",
                "bruises",
                "odor",
                "gill_attachment",
                "gill_spacing",
                "gill_size",
                "gill_color",
                "stalk_shape",
                "stalk_root",
                "stalk_surface_above_ring",
                "stalk_surface_below_ring",
                "stalk_color_above_ring",
                "stalk_color_below_ring",
                "veil_type",
                "veil_color",
                "ring_number",
                "ring_type",
                "spore_print_color",
                "population",
                "habitat"
            ]
            # Make sure we have the right number of columns
            if len(columns) != df.shape[1]:
                print(f"[{dataset_name}] Warning: Expected {len(columns)} columns but got {df.shape[1]}")
                # Adjust columns to match the data
                if len(columns) > df.shape[1]:
                    columns = columns[:df.shape[1]]
                else:
                    # Add generic names for extra columns
                    for i in range(df.shape[1] - len(columns)):
                        columns.append(f"extra_{i+1}")
            
            df.columns = columns
            print(f"[{dataset_name}] Assigned column names")
        
        # Log details
        print(f"[{dataset_name}] DataFrame shape: {df.shape}")
        print(f"[{dataset_name}] Data types of columns:\n{df.dtypes}")
        print(f"[{dataset_name}] First 5 rows:\n{df.head().to_string()}")
        
        # Convert 'class' to binary 'target': p => 1, e => 0
        # Check if 'class' column exists - this is critical for this dataset
        if "class" not in df.columns:
            # Look for the class in the first column
            first_col = df.columns[0]
            if df[first_col].isin(['p', 'e']).all():
                # This is likely the class column with a different name
                print(f"[{dataset_name}] Found class values in column '{first_col}', renaming to 'class'")
                df.rename(columns={first_col: 'class'}, inplace=True)
            else:
                # Search all columns for p/e values
                class_column = None
                for col in df.columns:
                    if df[col].isin(['p', 'e']).all() or df[col].isin(['p', 'e']).mean() > 0.8:
                        class_column = col
                        break
                
                if class_column:
                    print(f"[{dataset_name}] Found class values in column '{class_column}', renaming to 'class'")
                    df.rename(columns={class_column: 'class'}, inplace=True)
                else:
                    raise ValueError(f"[{dataset_name}] Could not find a column with class values (p/e)")
        
        if "class" in df.columns and "target" not in df.columns:
            df["target"] = df["class"].apply(lambda c: 1 if c == 'p' else 0)
            df.drop(columns=["class"], inplace=True)
            print(f"[{dataset_name}] Converted 'class' to binary 'target' (0: edible, 1: poisonous)")
        elif "target" not in df.columns:
            raise ValueError(f"[{dataset_name}] No 'class' column found to convert to target.")
        
        # Replace '?' with NaN, handle missing values
        df.replace('?', pd.NA, inplace=True)
        print(f"[{dataset_name}] Checking for missing values:")
        for col in df.columns:
            missing = df[col].isna().sum()
            print(f"  - {col}: {missing} missing")
        
        # Drop rows with missing values
        initial_length = len(df)
        df.dropna(axis=0, how="any", inplace=True)
        dropped = initial_length - len(df)
        if dropped > 0:
            print(f"[{dataset_name}] Dropped {dropped} rows due to missing values.")
        
        # Convert categorical columns to numeric
        print(f"[{dataset_name}] Converting categorical features to numeric...")
        for col in df.columns:
            if col != 'target' and df[col].dtype == 'object':
                # Use label encoding for categorical features
                df[col] = pd.Categorical(df[col]).codes
                print(f"  - Encoded {col}")
        
        # Convert all integer columns to float64 to avoid imputer casting issues
        for col in df.columns:
            if df[col].dtype.kind in 'iu':  # integer types
                df[col] = df[col].astype('float64')
        
        # Shuffle dataset
        print(f"[{dataset_name}] Shuffling the dataset randomly...")
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        print(f"[{dataset_name}] Dataset shuffled and index reset.")
        
        # Final logs
        print(f"[{dataset_name}] Final DataFrame shape: {df.shape}")
        
        # Distribution of the target (0=edible, 1=poisonous)
        target_counts = df["target"].value_counts()
        print(f"[{dataset_name}] Target distribution:")
        print(f"  - Class 0 (edible):    {target_counts.get(0, 0)}")
        print(f"  - Class 1 (poisonous): {target_counts.get(1, 0)}")
        
        print(f"[{dataset_name}] Example of first 5 shuffled rows:\n{df.head().to_string()}")
        
        return df

# For testing
if __name__ == "__main__":
    dataset = MushroomDataset()
    data = dataset.get_data()
    print(f"Dataset loaded successfully with {len(data)} rows.")

