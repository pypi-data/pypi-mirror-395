import os
import pandas as pd
import io
from sklearn.datasets import load_breast_cancer
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class BreastCancerDataset(BaseDatasetLoader):
    """
    Breast Cancer Wisconsin (Diagnostic) dataset.
    Classification: Binary (malignant/benign tumors)
    Features: 30 numeric features from digitized images of breast mass
    Source: Scikit-learn built-in dataset
    """
    
    def get_dataset_info(self):
        """Dataset metadata for the loader framework"""
        return {
            'name': 'BreastCancerDataset',
            'source_id': 'sklearn:breast_cancer',  # Unique identifier 
            'category': 'binary_classification',
            'description': 'Wisconsin Breast Cancer Dataset: 569 samples, 30 features. Binary classification (malignant/benign).',
        }
    
    def download_dataset(self, info):
        """Generate dataset from scikit-learn"""
        # Load dataset from scikit-learn
        data = load_breast_cancer()
        df = pd.DataFrame(data.data, columns=data.feature_names)
        
        # Invert target: scikit-learn has 0 as malignant, 1 as benign; we set 1 as malignant
        df['target'] = 1 - data.target
        
        # Convert to CSV bytes
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        return csv_buffer.getvalue().encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the dataset into final form"""
        dataset_name = info['name']
        
        # Log DataFrame details
        print(f"[{dataset_name}] DataFrame shape: {df.shape}")
        print(f"[{dataset_name}] Data types of columns:\n{df.dtypes}")
        print(f"[{dataset_name}] First 5 rows of the DataFrame:\n{df.head(5).to_string()}")
        
        # Check for missing values
        print(f"[{dataset_name}] Missing values per column:")
        for col in df.columns:
            missing = df[col].isna().sum()
            print(f"  - {col}: {missing} missing values ({100 * missing / len(df):.2f}%)")
        
        # Log target distribution
        target_counts = df['target'].value_counts(dropna=False)
        print(f"[{dataset_name}] Target distribution:")
        print(f"  - Class 0 (benign): {target_counts.get(0, 0)} instances ({100 * target_counts.get(0, 0) / len(df):.2f}%)")
        print(f"  - Class 1 (malignant): {target_counts.get(1, 0)} instances ({100 * target_counts.get(1, 0) / len(df):.2f}%)")
        print(f"  - NaN values: {df['target'].isna().sum()} instances ({100 * df['target'].isna().sum() / len(df):.2f}%)")
        
        # Shuffle dataset (consistent with original code)
        print(f"[{dataset_name}] Shuffling the dataset randomly...")
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        print(f"[{dataset_name}] Dataset shuffled and indexes reset.")
        
        # Final logging
        print(f"[{dataset_name}] Final DataFrame shape: {df.shape}")
        print(f"[{dataset_name}] Sample of first 5 rows:\n{df.head(5).to_string()}")
        
        return df

# Example usage (for testing purposes; remove in production)
if __name__ == "__main__":
    dataset = BreastCancerDataset()
    df = dataset.get_data()
    print(f"Dataset loaded successfully with {len(df)} rows.")
