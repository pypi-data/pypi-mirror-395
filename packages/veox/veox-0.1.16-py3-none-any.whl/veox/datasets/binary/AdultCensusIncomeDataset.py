import io
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader


class AdultCensusIncomeDataset(BaseDatasetLoader):
    """
    UCI Adult Census Income dataset.
    Binary classification: income >50K (1) vs <=50K (0)
    ~48k instances, 14 features (mixed types)
    Source: UCI repository
    """

    def get_dataset_info(self):
        return {
            "name": "AdultCensusIncomeDataset",
            "source_id": "uci:adult_census_income",
            "category": "binary_classification",
            "description": "Adult Census Income dataset from UCI (mixed categorical/numeric).",
        }

    def download_dataset(self, info):
        """Download the Adult Census Income dataset from UCI or GitHub"""
        # Prefer pre-processed CSV from vega-datasets (main branch). Fallback to UCI raw if unavailable.
        session = requests.Session()
        session.trust_env = False

        urls = [
            "https://raw.githubusercontent.com/vega/vega-datasets/main/data/adult.csv",
            # UCI raw adult.data (no header); we will add names and parse below if used
            "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data",
        ]

        last_err = None
        for url in urls:
            try:
                r = session.get(url, timeout=30)
                r.raise_for_status()
                raw = r.content
                if url.endswith("adult.csv"):
                    df = pd.read_csv(io.BytesIO(raw))
                    print(f"[AdultCensusIncomeDataset] Downloaded {df.shape[0]} rows from GitHub")
                    return df.to_csv(index=False).encode('utf-8')
                else:
                    # UCI adult.data
                    cols = [
                        "age",
                        "workclass",
                        "fnlwgt",
                        "education",
                        "education_num",
                        "marital_status",
                        "occupation",
                        "relationship",
                        "race",
                        "sex",
                        "capital_gain",
                        "capital_loss",
                        "hours_per_week",
                        "native_country",
                        "income",
                    ]
                    df = pd.read_csv(
                        io.BytesIO(raw),
                        header=None,
                        names=cols,
                        skipinitialspace=True,
                        na_values=["?"],
                    )
                    print(f"[AdultCensusIncomeDataset] Downloaded {df.shape[0]} rows from UCI")
                    return df.to_csv(index=False).encode('utf-8')
            except Exception as e:
                last_err = e
                continue
        if last_err:
            raise last_err
        raise RuntimeError("Failed to download Adult dataset from all sources")

    def process_dataframe(self, df: pd.DataFrame, info):
        dataset_name = info["name"]
        
        # Normalize column names
        df.columns = [str(c).strip().replace(" ", "_") for c in df.columns]
        
        # Map label to binary target
        label_col = "income"
        if label_col not in df.columns:
            # Some variants may use 'class' or 'Target'
            for alt in ["class", "target", "Target", "income>50K"]:
                if alt in df.columns:
                    label_col = alt
                    break
        if label_col not in df.columns:
            raise ValueError(f"[{dataset_name}] Adult dataset missing label column")
        
        # Handle both string and numeric income values
        if df[label_col].dtype == 'object':
            df["target"] = df[label_col].astype(str).str.strip().str.rstrip('.').str.contains(">50K").astype(int)
        else:
            # If numeric, assume >50K threshold
            df["target"] = (df[label_col] > 50).astype(int)
        
        # Drop the original label
        df = df.drop(columns=[label_col])
        
        # Convert categorical columns to numeric
        categorical_cols = ['workclass', 'education', 'marital_status', 'marital-status', 
                          'occupation', 'relationship', 'race', 'sex', 'native_country', 'native-country']
        
        for col in categorical_cols:
            if col in df.columns:
                # Handle missing values represented as ' ?'
                if df[col].dtype == 'object':
                    df[col] = df[col].astype(str).str.strip()
                    df[col] = df[col].replace('?', pd.NA)
                    # Label encoding
                    df[col] = pd.Categorical(df[col]).codes
        
        # Ensure all numeric columns are properly typed
        numeric_cols = ['age', 'fnlwgt', 'education_num', 'education-num', 
                       'capital_gain', 'capital-gain', 'capital_loss', 'capital-loss', 
                       'hours_per_week', 'hours-per-week']
        for col in numeric_cols:
            if col in df.columns:
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
        
        # Ensure target is last
        cols = [c for c in df.columns if c != "target"] + ["target"]
        df = df[cols]
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[{dataset_name}] Final shape: {df.shape}")
        print(f"[{dataset_name}] Target distribution: {df['target'].value_counts().to_dict()}")
        return df

if __name__ == "__main__":
    ds = AdultCensusIncomeDataset()
    frame = ds.get_data()
    print(frame.head())
    print(f"Target column: {frame.columns[-1]}")
    print(frame['target'].value_counts()) 