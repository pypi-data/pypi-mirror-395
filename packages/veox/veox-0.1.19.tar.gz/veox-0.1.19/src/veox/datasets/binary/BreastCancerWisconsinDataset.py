import pandas as pd
from app.datasets.BaseDatasetLoader import BaseDatasetLoader


class BreastCancerWisconsinDataset(BaseDatasetLoader):
    """
    Breast Cancer Wisconsin (Diagnostic) dataset.
    Binary classification: malignant (1) vs benign (0)
    569 instances, 30 features
    Source: scikit-learn datasets (load_breast_cancer)
    """

    def get_dataset_info(self):
        return {
            "name": "BreastCancerWisconsinDataset",
            "source_id": "sklearn:load_breast_cancer",
            "category": "binary_classification",
            "description": "Breast Cancer Wisconsin Diagnostic dataset from scikit-learn (569x30).",
        }

    def download_dataset(self, info):
        from sklearn.datasets import load_breast_cancer

        ds = load_breast_cancer()
        X = pd.DataFrame(ds.data, columns=list(ds.feature_names))
        y = pd.Series(ds.target, name="target")
        df = pd.concat([X, y], axis=1)
        return df

    def process_dataframe(self, df: pd.DataFrame, info):
        # Ensure target is at the end and is binary int
        if "target" not in df.columns:
            raise ValueError("Expected 'target' column in dataframe")
        df["target"] = df["target"].astype(int)
        if df.columns[-1] != "target":
            cols = [c for c in df.columns if c != "target"] + ["target"]
            df = df[cols]
        return df


