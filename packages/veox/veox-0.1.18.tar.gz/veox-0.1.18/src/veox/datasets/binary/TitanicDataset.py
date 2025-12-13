import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader


class TitanicDataset(BaseDatasetLoader):
    """Titanic Passenger Survival dataset.

    Binary classification task: predict survival of passengers.
    Original columns include passenger demographics, ticket info, etc.
    The raw dataset already contains a `Survived` column (0 = died, 1 = survived).
    We convert this to `target` (0/1) and place it as the *last* column.
    """

    def get_dataset_info(self):
        return {
            "name": "TitanicDataset",
            "source_id": "uci:titanic_survival",  # unique-ish identifier
            "category": "binary_classification",
            "description": "Titanic passenger survival dataset. Binary target indicating survival (1) or death (0).",
        }

    def download_dataset(self, info):
        dataset_name = info["name"]
        # Public mirror of the classic Titanic CSV (includes header)
        url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
        print(f"[{dataset_name}] Downloading from URL: {url}")

        try:
            r = requests.get(url, timeout=30)
            print(f"[{dataset_name}] HTTP response status: {r.status_code}")
            if r.status_code != 200:
                raise Exception(f"Failed to download dataset: HTTP {r.status_code}")

            file_size = len(r.content)
            print(f"[{dataset_name}] Download complete. File size: {file_size} bytes")
            if file_size < 10000:  # simple sanity-check (~60 KB expected)
                first_lines = r.content.decode("utf-8", errors="replace").splitlines()[:5]
                print(f"[{dataset_name}] File suspiciously small. First lines:\n{os.linesep.join(first_lines)}")
                raise Exception("Downloaded file too small; possible fetch error.")
            return r.content
        except Exception as exc:
            print(f"[{dataset_name}] Download failed: {exc}")
            raise

    def process_dataframe(self, df, info):
        dataset_name = info["name"]

        print(f"[{dataset_name}] Raw DataFrame shape: {df.shape}")

        # Ensure Survived column exists -> create target
        if "Survived" not in df.columns:
            # If not, maybe the first row was taken as header when loading from cache without header
            # Fallback: assume last column is target and rename
            print(f"[{dataset_name}] 'Survived' column missing – assuming last column is target.")
            df.rename(columns={df.columns[-1]: "Survived"}, inplace=True)

        df["target"] = pd.to_numeric(df["Survived"], errors="coerce").fillna(0).astype(int)
        df.drop(columns=["Survived"], inplace=True)

        # Drop non-feature columns
        drop_cols = ['PassengerId', 'Name', 'Ticket', 'Cabin']
        for col in drop_cols:
            if col in df.columns:
                print(f"[{dataset_name}] Dropping '{col}' column")
                df.drop(columns=[col], inplace=True)

        # Convert categorical columns to numeric
        print(f"[{dataset_name}] Converting categorical columns to numeric...")
        for col in df.columns:
            if col != 'target' and df[col].dtype == 'object':
                # Handle Sex column specially
                if col == 'Sex':
                    df[col] = df[col].map({'male': 1, 'female': 0})
                    print(f"  - Converted {col} to binary")
                elif col == 'Embarked':
                    # Embarked has C, Q, S values
                    df[col] = df[col].map({'C': 0, 'Q': 1, 'S': 2})
                    print(f"  - Converted {col} to numeric")
                else:
                    # Other categorical columns
                    df[col] = pd.Categorical(df[col]).codes
                    print(f"  - Encoded {col}")

        # Basic NA handling: drop rows missing target or all-NA rows
        df.dropna(axis=0, how="all", inplace=True)

        # Simple numeric imputation (median) for numeric cols to avoid dropping many rows
        # Fix the pandas FutureWarning by using .loc and proper assignment
        numeric_cols = df.select_dtypes(include=["number"]).columns.difference(["target"])
        for col in numeric_cols:
            median_value = df[col].median()
            df.loc[:, col] = df[col].fillna(median_value)

        # Drop rows where target is NA (shouldn't happen)
        df = df[df["target"].notna()]

        # Reorder columns so target is **last**
        other_cols = [c for c in df.columns if c != "target"]
        df = df[other_cols + ["target"]]

        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)

        print(f"[{dataset_name}] Final DataFrame shape: {df.shape}")
        print(f"[{dataset_name}] Target distribution: {df['target'].value_counts().to_dict()}")
        return df


if __name__ == "__main__":
    ds = TitanicDataset()
    frame = ds.get_data()
    print(f"Loaded TitanicDataset with {len(frame)} rows and {len(frame.columns)} columns") 