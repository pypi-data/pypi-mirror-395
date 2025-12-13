import pandas as pd
import importlib
from pathlib import Path
from typing import Tuple, Optional, List, Dict, Any
import veox.datasets.base  # Ensure shim is loaded
import pkgutil
import veox.datasets.binary
import veox.datasets.regression


class DatasetLoader:
    """Load built-in datasets from Veox package."""

    def __init__(self):
        self._dataset_cache = {}

    def load_dataset(self, name: str) -> Tuple[pd.DataFrame, pd.Series]:
        """Load a built-in dataset by name."""
        if name in self._dataset_cache:
            return self._dataset_cache[name]

        # Try to import the dataset class
        try:
            # Normalize name (remove 'Dataset' suffix if present)
            base_name = name.replace('Dataset', '') if name.endswith('Dataset') else name

            # Try binary first, then regression
            dataset_class = None
            for category in ['binary', 'regression']:
                try:
                    module_name = f"veox.datasets.{category}.{base_name}Dataset"
                    module = importlib.import_module(module_name)
                    dataset_class = getattr(module, f"{base_name}Dataset")
                    break
                except (ImportError, AttributeError) as e:
                    print(f"DEBUG: Failed to import {module_name}: {e}")
                    continue

            
            if not dataset_class:
                raise ValueError(f"Dataset '{name}' not found in built-in datasets")

            # Instantiate and load
            dataset = dataset_class()
            # Note: get_data() might fail if it relies on download_dataset and we haven't implemented it.
            # We need to check if the dataset class implements get_data or inherits it.
            # If it inherits, we need to ensure our BaseDatasetLoader shim works.
            df = dataset.get_data()

            # Split into X, y
            if 'target' in df.columns:
                X = df.drop('target', axis=1)
                y = df['target']
            else:
                # Assume last column is target if not named 'target'
                # But most DOUG datasets have a target column defined in metadata
                # We should check metadata if possible
                info = dataset.get_dataset_info()
                target_col = info.get('target_column', 'target')
                if target_col in df.columns:
                    X = df.drop(target_col, axis=1)
                    y = df[target_col]
                else:
                    X = df.iloc[:, :-1]
                    y = df.iloc[:, -1]

            # Cache the result
            self._dataset_cache[name] = (X, y)
            return X, y

        except Exception as e:
            raise ValueError(f"Failed to load dataset '{name}': {e}")

    def list_datasets(self) -> List[Dict[str, Any]]:
        """List all available built-in datasets."""
        datasets = []
        
        for category, package in [('binary', veox.datasets.binary), ('regression', veox.datasets.regression)]:
            try:
                for _, name, _ in pkgutil.iter_modules(package.__path__):
                    if name.endswith('Dataset'):
                        # Try to import and get info
                        try:
                            module_name = f"veox.datasets.{category}.{name}"
                            module = importlib.import_module(module_name)
                            dataset_class = getattr(module, name)
                            
                            # Instantiate to get info (lightweight hopefully)
                            ds_instance = dataset_class()
                            info = ds_instance.get_dataset_info()
                            
                            datasets.append({
                                "name": name,
                                "description": info.get('description', 'No description'),
                                "task": category,
                                "n_samples": info.get('n_samples', 'Unknown'),
                                "n_features": info.get('n_features', 'Unknown')
                            })
                        except Exception as e:
                            # Skip if load fails
                            pass
            except Exception:
                pass
                
        return sorted(datasets, key=lambda x: x['name'])

# Convenience functions (sklearn-style)
def load_heart_disease() -> Tuple[pd.DataFrame, pd.Series]:
    """Load Heart Disease dataset."""
    loader = DatasetLoader()
    return loader.load_dataset("HeartDiseaseDataset")

def load_titanic() -> Tuple[pd.DataFrame, pd.Series]:
    """Load Titanic dataset."""
    loader = DatasetLoader()
    return loader.load_dataset("TitanicDataset")

def load_boston_housing() -> Tuple[pd.DataFrame, pd.Series]:
    """Load Boston Housing dataset."""
    loader = DatasetLoader()
    return loader.load_dataset("BostonHousingDataset")
