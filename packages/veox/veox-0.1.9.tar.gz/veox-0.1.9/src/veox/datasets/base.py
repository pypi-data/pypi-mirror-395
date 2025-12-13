import sys
import types
import io
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional

# --- Lightweight shim for seed_data modules that import app.datasets.BaseDatasetLoader ---
# This allows us to copy dataset files from DOUG directly without modification
if "app.datasets" not in sys.modules:
    # Ensure root package exists
    sys.modules.setdefault("app", types.ModuleType("app"))
    ds_mod = types.ModuleType("app.datasets")
    sys.modules["app.datasets"] = ds_mod

    class BaseDatasetLoader:
        """Minimal BaseDatasetLoader to satisfy seed_data dataset modules."""

        def __init__(self):
            self.cache_file: Optional[Path] = None

        def get_dataset_info(self) -> Dict[str, Any]:
            return {"name": self.__class__.__name__}

        def download_dataset(self, info: Dict[str, Any]):
            raise NotImplementedError("download_dataset not implemented in stub")

        def process_dataframe(self, df, info: Dict[str, Any]):
            return df

        def _coerce_dataframe(self, payload):
            if isinstance(payload, pd.DataFrame):
                return payload
            if isinstance(payload, (bytes, bytearray)):
                try:
                    return pd.read_csv(io.BytesIO(payload))
                except:
                    return pd.read_parquet(io.BytesIO(payload))
            if isinstance(payload, str):
                try:
                    return pd.read_csv(io.StringIO(payload))
                except:
                    pass
            return payload

        def get_data(self):
            info = self.get_dataset_info()
            name = info['name']
            
            # Setup cache
            cache_dir = Path.home() / ".veox" / "datasets"
            cache_dir.mkdir(parents=True, exist_ok=True)
            cache_file = cache_dir / f"{name}.csv"
            
            if cache_file.exists():
                # Load from cache
                try:
                    df = pd.read_csv(cache_file)
                    # Simple check if it looks right (optional)
                    return df
                except Exception:
                    pass # Re-download if cache is corrupt

            # Download
            try:
                raw_data = self.download_dataset(info)
                
                # Coerce to DataFrame
                df = self._coerce_dataframe(raw_data)
                
                # Process
                df = self.process_dataframe(df, info)
                
                # Cache
                df.to_csv(cache_file, index=False)
                
                return df
            except Exception as e:
                raise RuntimeError(f"Failed to load dataset {name}: {e}")


    # Inject into sys.modules so imports work
    # The dataset files use: from app.datasets.BaseDatasetLoader import BaseDatasetLoader
    # So app.datasets.BaseDatasetLoader must be a module containing BaseDatasetLoader class
    
    bdl_mod = types.ModuleType("app.datasets.BaseDatasetLoader")
    bdl_mod.BaseDatasetLoader = BaseDatasetLoader
    sys.modules["app.datasets.BaseDatasetLoader"] = bdl_mod
    
    # Also allow from app.datasets import BaseDatasetLoader
    ds_mod.BaseDatasetLoader = BaseDatasetLoader

