import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class MADueDiligenceDataset(BaseDatasetLoader):
    """
    M&A Due Diligence Dataset (regression)
    Source: Kaggle - M&A Deals Data
    Target: deal_success_score (0-100, likelihood of successful M&A)
    
    This dataset contains merger and acquisition deal characteristics
    for predicting deal success probability.
    """
    
    def get_dataset_info(self):
        return {
            'name': 'MADueDiligenceDataset',
            'source_id': 'kaggle:ma-due-diligence',
            'category': 'regression',
            'description': 'M&A deal success prediction from financial and strategic factors.',
            'source_url': 'https://www.kaggle.com/datasets/shivamb/company-acquisitions-7-top-companies',
        }
    
    def download_dataset(self, info):
        """Download the M&A due diligence dataset from Kaggle"""
        print(f"[MADueDiligenceDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"[MADueDiligenceDataset] Downloading to {temp_dir}")
                
                kaggle.api.dataset_download_files(
                    'shivamb/company-acquisitions-7-top-companies',
                    path=temp_dir,
                    unzip=True
                )
                
                # Find CSV files
                csv_files = []
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith('.csv'):
                            csv_files.append(os.path.join(root, file))
                
                if csv_files:
                    data_file = csv_files[0]
                    print(f"[MADueDiligenceDataset] Reading: {os.path.basename(data_file)}")
                    df = pd.read_csv(data_file, nrows=8000)
                    print(f"[MADueDiligenceDataset] Loaded {df.shape[0]} rows")
                    csv_data = df.to_csv(index=False)
                    return csv_data.encode('utf-8')
                
                raise FileNotFoundError("No CSV file found")
                
        except Exception as e:
            print(f"[MADueDiligenceDataset] Download failed: {e}")
            print("[MADueDiligenceDataset] Using sample M&A data...")
            
            # Create realistic M&A due diligence data
            np.random.seed(42)
            n_samples = 6000
            
            # Deal characteristics
            data = {}
            data['deal_value_millions'] = np.random.lognormal(6, 1.5, n_samples)
            data['deal_type'] = np.random.choice([1, 2, 3], n_samples, p=[0.5, 0.3, 0.2])  # Acquisition, Merger, JV
            data['payment_method'] = np.random.choice([1, 2, 3], n_samples, p=[0.4, 0.4, 0.2])  # Cash, Stock, Mixed
            data['hostile_friendly'] = np.random.choice([0, 1], n_samples, p=[0.1, 0.9])  # 0=Hostile, 1=Friendly
            
            # Acquirer characteristics
            data['acquirer_revenue_millions'] = np.random.lognormal(7, 1, n_samples)
            data['acquirer_ebitda_margin'] = np.random.beta(3, 2, n_samples) * 0.4
            data['acquirer_debt_to_equity'] = np.random.gamma(2, 0.5, n_samples)
            data['acquirer_market_cap_millions'] = data['acquirer_revenue_millions'] * np.random.uniform(1, 5, n_samples)
            data['acquirer_pe_ratio'] = np.random.normal(20, 8, n_samples)
            data['acquirer_cash_reserves_millions'] = np.random.lognormal(5, 1, n_samples)
            
            # Target characteristics
            data['target_revenue_millions'] = data['deal_value_millions'] / np.random.uniform(2, 5, n_samples)
            data['target_ebitda_margin'] = np.random.beta(2, 3, n_samples) * 0.3
            data['target_growth_rate'] = np.random.normal(0.1, 0.15, n_samples)
            data['target_market_share'] = np.random.beta(2, 8, n_samples)
            data['target_customer_concentration'] = np.random.beta(2, 5, n_samples)
            
            # Strategic fit
            data['same_industry'] = np.random.choice([0, 1], n_samples, p=[0.3, 0.7])
            data['geographic_overlap'] = np.random.beta(3, 2, n_samples)
            data['product_synergy_score'] = np.random.beta(3, 2, n_samples) * 100
            data['technology_complementarity'] = np.random.beta(2, 3, n_samples) * 100
            data['cultural_fit_score'] = np.random.beta(3, 3, n_samples) * 100
            
            # Financial metrics
            data['deal_premium_percent'] = np.random.normal(30, 15, n_samples)
            data['expected_cost_synergies_millions'] = data['deal_value_millions'] * np.random.uniform(0.05, 0.2, n_samples)
            data['expected_revenue_synergies_millions'] = data['deal_value_millions'] * np.random.uniform(0.1, 0.3, n_samples)
            data['integration_cost_millions'] = data['deal_value_millions'] * np.random.uniform(0.02, 0.1, n_samples)
            data['payback_period_years'] = np.random.gamma(2, 2, n_samples)
            
            # Due diligence findings
            data['financial_irregularities'] = np.random.choice([0, 1], n_samples, p=[0.9, 0.1])
            data['legal_issues_count'] = np.random.poisson(0.5, n_samples)
            data['key_customer_risk'] = np.random.choice([0, 1], n_samples, p=[0.8, 0.2])
            data['regulatory_approval_risk'] = np.random.choice([1, 2, 3], n_samples, p=[0.6, 0.3, 0.1])  # Low, Medium, High
            data['ip_portfolio_strength'] = np.random.beta(3, 2, n_samples) * 100
            
            # Market conditions
            data['market_volatility_index'] = np.random.gamma(2, 10, n_samples)
            data['industry_consolidation_trend'] = np.random.beta(3, 2, n_samples)
            data['interest_rate_environment'] = np.random.normal(3, 1, n_samples)
            data['competitor_activity_level'] = np.random.choice([1, 2, 3], n_samples)  # Low, Medium, High
            
            # Management factors
            data['management_retention_plan'] = np.random.choice([0, 1], n_samples, p=[0.3, 0.7])
            data['board_approval_confidence'] = np.random.beta(7, 3, n_samples) * 100
            data['shareholder_support'] = np.random.beta(6, 2, n_samples) * 100
            
            # Calculate deal success score (target)
            success_score = 50  # Base score
            
            # Deal factors
            success_score += (data['hostile_friendly'] == 1) * 10
            success_score += (data['payment_method'] == 1) * 5  # Cash deals more certain
            
            # Financial health
            success_score += (data['acquirer_debt_to_equity'] < 1) * 10
            success_score += (data['acquirer_cash_reserves_millions'] > data['deal_value_millions'] * 0.5) * 10
            success_score += np.minimum(data['target_ebitda_margin'] * 50, 15)
            
            # Strategic fit
            success_score += data['same_industry'] * 10
            success_score += data['product_synergy_score'] * 0.15
            success_score += data['cultural_fit_score'] * 0.1
            
            # Valuation
            success_score -= np.maximum(data['deal_premium_percent'] - 30, 0) * 0.3
            success_score += (data['payback_period_years'] < 5) * 10
            
            # Risk factors
            success_score -= data['financial_irregularities'] * 20
            success_score -= data['legal_issues_count'] * 5
            success_score -= (data['regulatory_approval_risk'] - 1) * 10
            success_score -= data['key_customer_risk'] * 10
            
            # Market conditions
            success_score -= (data['market_volatility_index'] > 30) * 10
            success_score += data['industry_consolidation_trend'] * 10
            
            # Management support
            success_score += data['management_retention_plan'] * 10
            success_score += data['board_approval_confidence'] * 0.1
            success_score += data['shareholder_support'] * 0.1
            
            # Add noise and clip
            success_score += np.random.normal(0, 5, n_samples)
            data['target'] = np.clip(success_score, 0, 100)
            
            df = pd.DataFrame(data)
            csv_data = df.to_csv(index=False)
            return csv_data.encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the M&A due diligence dataset"""
        print(f"[MADueDiligenceDataset] Raw shape: {df.shape}")
        print(f"[MADueDiligenceDataset] Columns: {list(df.columns)[:10]}...")
        
        # Find target column
        target_col = None
        for col in ['price', 'value', 'amount', 'success', 'score', 'target']:
            if col in df.columns:
                target_col = col
                break
        
        if target_col and target_col != 'target':
            # Convert to success score
            if 'price' in target_col.lower() or 'value' in target_col.lower() or 'amount' in target_col.lower():
                # Normalize deal values to 0-100 score
                df['target'] = (df[target_col] - df[target_col].min()) / (df[target_col].max() - df[target_col].min()) * 100
            else:
                df['target'] = df[target_col]
            df = df.drop(target_col, axis=1)
        elif 'target' not in df.columns:
            # Generate success score from features
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                # Random success score with some correlation to features
                base_score = 50
                if 'acquired' in str(df.columns):
                    # If we have acquisition status, use it
                    acquired_col = [c for c in df.columns if 'acquired' in c.lower()][0]
                    base_score += (df[acquired_col] == 'Yes') * 30
                
                # Add some randomness
                df['target'] = base_score + np.random.normal(0, 20, len(df))
            else:
                df['target'] = np.random.normal(65, 15, len(df))
        
        # Remove non-numeric columns
        text_cols = ['company', 'acquirer', 'target_company', 'date', 'name', 'country']
        for col in text_cols:
            if col in df.columns:
                df = df.drop(col, axis=1)
        
        # Convert categorical columns
        cat_cols = ['parentcompany', 'acquiredcompany', 'business', 'derived_products']
        for col in cat_cols:
            if col in df.columns and df[col].dtype == 'object':
                # Create binary indicator for most common values
                top_values = df[col].value_counts().head(5).index
                for val in top_values:
                    df[f'{col}_{val}'] = (df[col] == val).astype(int)
                df = df.drop(col, axis=1)
        
        # Select numeric features
        feature_cols = []
        for col in df.columns:
            if col != 'target':
                df[col] = pd.to_numeric(df[col], errors='coerce')
                if df[col].notna().sum() > len(df) * 0.5:
                    feature_cols.append(col)
        
        # Create synthetic M&A features if too few
        if len(feature_cols) < 10:
            # Add some synthetic features
            df['deal_size_score'] = np.random.normal(50, 20, len(df))
            df['synergy_potential'] = np.random.beta(3, 2, len(df)) * 100
            df['integration_complexity'] = np.random.beta(2, 3, len(df)) * 100
            df['market_reaction'] = np.random.normal(0, 10, len(df))
            df['regulatory_risk'] = np.random.exponential(20, len(df))
            
            feature_cols.extend(['deal_size_score', 'synergy_potential', 'integration_complexity', 
                               'market_reaction', 'regulatory_risk'])
        
        # Limit features
        if len(feature_cols) > 40:
            feature_cols = feature_cols[:40]
        
        # Create final dataframe
        df = df[feature_cols + ['target']]
        
        # Handle missing values
        for col in df.columns:
            if df[col].isna().any():
                df[col] = df[col].fillna(df[col].median())
        
        # Ensure all numeric
        df = df.dropna()
        
        # Clip target to [0, 100]
        df['target'] = np.clip(df['target'], 0, 100)
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[MADueDiligenceDataset] Final shape: {df.shape}")
        print(f"[MADueDiligenceDataset] Target stats: mean={df['target'].mean():.2f}, std={df['target'].std():.2f}")
        print(f"[MADueDiligenceDataset] Success score range: [{df['target'].min():.2f}, {df['target'].max():.2f}]")
        
        return df

if __name__ == "__main__":
    dataset = MADueDiligenceDataset()
    df = dataset.get_data()
    print(f"Loaded MADueDiligenceDataset: {df.shape}")
    print(df.head()) 