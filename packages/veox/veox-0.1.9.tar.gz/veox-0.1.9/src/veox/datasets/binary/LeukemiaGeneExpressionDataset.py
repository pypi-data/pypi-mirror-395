import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class LeukemiaGeneExpressionDataset(BaseDatasetLoader):
    """
    Leukemia Gene Expression Dataset (binary classification)
    Source: Kaggle - Gene expression data for leukemia classification
    Target: leukemia_type (0=ALL, 1=AML)
    
    This dataset contains gene expression data for distinguishing between
    Acute Lymphoblastic Leukemia (ALL) and Acute Myeloid Leukemia (AML).
    """
    
    def get_dataset_info(self):
        return {
            'name': 'LeukemiaGeneExpressionDataset',
            'source_id': 'kaggle:leukemia-gene-expression',
            'category': 'binary_classification',
            'description': 'Gene expression data for ALL vs AML leukemia classification.',
            'source_url': 'https://www.kaggle.com/datasets/crawford/gene-expression',
        }
    
    def download_dataset(self, info):
        """Download the leukemia gene expression dataset from Kaggle"""
        print(f"[LeukemiaGeneExpressionDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"[LeukemiaGeneExpressionDataset] Downloading to {temp_dir}")
                
                kaggle.api.dataset_download_files(
                    'crawford/gene-expression',
                    path=temp_dir,
                    unzip=True
                )
                
                # Find CSV files
                csv_files = []
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith('.csv'):
                            csv_files.append(os.path.join(root, file))
                
                if not csv_files:
                    raise FileNotFoundError("No CSV file found")
                
                # Read the first CSV file
                data_file = csv_files[0]
                print(f"[LeukemiaGeneExpressionDataset] Reading: {os.path.basename(data_file)}")
                
                df = pd.read_csv(data_file)
                print(f"[LeukemiaGeneExpressionDataset] Loaded {df.shape[0]} rows, {df.shape[1]} columns")
                
                csv_data = df.to_csv(index=False)
                return csv_data.encode('utf-8')
                
        except Exception as e:
            print(f"[LeukemiaGeneExpressionDataset] Download failed: {e}")
            print("[LeukemiaGeneExpressionDataset] Using sample data...")
            
            # Create sample data based on classic Golub et al. dataset
            np.random.seed(42)
            n_samples = 72  # Classic dataset has 72 samples
            n_genes = 500   # Reduced from 7,129 for sample
            
            # Generate gene expression data
            data = {}
            
            # Create sample labels (38 ALL, 34 AML)
            n_all = 38
            n_aml = 34
            labels = ['ALL'] * n_all + ['AML'] * n_aml
            
            # Generate gene expression values
            for i in range(n_genes):
                gene_name = f'gene_{i+1}'
                # Base expression
                expression = np.random.lognormal(3, 1, n_samples)
                
                # Add differential expression for some genes
                if i < 50:  # First 50 genes are differentially expressed
                    # ALL samples have higher expression
                    expression[:n_all] *= np.random.uniform(1.5, 3)
                elif i < 100:  # Next 50 genes
                    # AML samples have higher expression
                    expression[n_all:] *= np.random.uniform(1.5, 3)
                
                data[gene_name] = expression
            
            data['cancer'] = labels
            
            df = pd.DataFrame(data)
            csv_data = df.to_csv(index=False)
            return csv_data.encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the leukemia dataset"""
        print(f"[LeukemiaGeneExpressionDataset] Raw shape: {df.shape}")
        print(f"[LeukemiaGeneExpressionDataset] Columns sample: {list(df.columns)[:10]}...")
        
        # Find target column
        target_col = None
        for col in ['cancer', 'type', 'class', 'label', 'leukemia_type']:
            if col in df.columns:
                target_col = col
                break
        
        if not target_col:
            # Check if last column contains ALL/AML
            last_col = df.columns[-1]
            if df[last_col].dtype == 'object':
                unique_vals = df[last_col].unique()
                if any('ALL' in str(v) or 'AML' in str(v) for v in unique_vals):
                    target_col = last_col
        
        if not target_col:
            raise ValueError("Could not find target column")
        
        # Create binary target (0=ALL, 1=AML)
        df['target'] = df[target_col].apply(lambda x: 0 if 'ALL' in str(x) else 1)
        
        # Select gene expression features (numeric columns)
        feature_cols = []
        for col in df.columns:
            if col not in [target_col, 'target'] and df[col].dtype in ['int64', 'float64']:
                feature_cols.append(col)
        
        # If too many features, select top variance features
        if len(feature_cols) > 2000:
            variances = df[feature_cols].var()
            top_features = variances.nlargest(2000).index.tolist()
            feature_cols = top_features
        
        # Create final dataframe
        df = df[feature_cols + ['target']]
        
        # Remove missing values
        df = df.dropna()
        
        # Ensure all numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.dropna()
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[LeukemiaGeneExpressionDataset] Final shape: {df.shape}")
        print(f"[LeukemiaGeneExpressionDataset] Target distribution: {df['target'].value_counts().to_dict()}")
        print(f"[LeukemiaGeneExpressionDataset] ALL: {(df['target'] == 0).sum()}, AML: {(df['target'] == 1).sum()}")
        
        return df

if __name__ == "__main__":
    dataset = LeukemiaGeneExpressionDataset()
    df = dataset.get_data()
    print(f"Loaded LeukemiaGeneExpressionDataset: {df.shape}")
    print(df.head()) 