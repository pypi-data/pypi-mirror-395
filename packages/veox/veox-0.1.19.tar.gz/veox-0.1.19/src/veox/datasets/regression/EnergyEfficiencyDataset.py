import os
import pandas as pd
import requests
import io
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class EnergyEfficiencyDataset(BaseDatasetLoader):
    """
    Loader for the Energy Efficiency dataset from the UCI Machine Learning Repository.
    
    This dataset contains building characteristics and their resulting energy performance 
    in terms of heating and cooling load. The datasets can be used for regression tasks
    to predict either heating load or cooling load.
    
    Features include relative compactness, surface area, wall area, roof area, etc.
    Target is the cooling load (energy efficiency).
    """

    def get_dataset_info(self):
        """Dataset metadata for the loader framework"""
        return {
            'name': 'EnergyEfficiencyDataset',
            'source_id': 'uci:energy_efficiency',  # Unique identifier
            'category': 'regression',
            'description': 'Energy Efficiency dataset: regression to predict cooling load based on building characteristics.',
        }
    
    def download_dataset(self, info):
        """Download dataset from UCI repository"""
        dataset_name = info['name']
        # URL for the Energy Efficiency dataset
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00242/ENB2012_data.xlsx"
        print(f"[{dataset_name}] Downloading from URL: {url}")
        
        try:
            r = requests.get(url, timeout=30)
            print(f"[{dataset_name}] HTTP response status: {r.status_code}")
            if r.status_code != 200:
                raise Exception(f"Failed to download dataset: HTTP {r.status_code}")
            
            file_size = len(r.content)
            print(f"[{dataset_name}] Download complete. File size: {file_size} bytes")
            
            if file_size < 10000:  # Sanity check for file size (xlsx larger)
                first_lines = r.content.decode("utf-8", errors="replace").splitlines()[:5]
                print(f"[{dataset_name}] File too small. First few lines:\n{os.linesep.join(first_lines)}")
                raise Exception(f"Downloaded file too small: {file_size} bytes. Expected >10 KB.")
            
            # Read Excel file directly and convert to CSV format    
            try:
                df = pd.read_excel(io.BytesIO(r.content), engine='openpyxl')
                print(f"[{dataset_name}] Successfully read Excel file with shape: {df.shape}")
                
                # Convert to CSV bytes
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False)
                csv_data = csv_buffer.getvalue().encode('utf-8')
                return csv_data
            except ImportError:
                print(f"[{dataset_name}] openpyxl not available, trying with xlrd...")
                try:
                    df = pd.read_excel(io.BytesIO(r.content), engine='xlrd')
                    print(f"[{dataset_name}] Successfully read Excel file with xlrd with shape: {df.shape}")
                    
                    # Convert to CSV bytes
                    csv_buffer = io.StringIO()
                    df.to_csv(csv_buffer, index=False)
                    csv_data = csv_buffer.getvalue().encode('utf-8')
                    return csv_data
                except Exception as e:
                    print(f"[{dataset_name}] Failed to read Excel with xlrd: {e}")
                    # Fall back to returning raw content which will trigger error handling
                    return r.content
            except Exception as e:
                print(f"[{dataset_name}] Failed to read Excel file: {e}")
                # Fall back to returning raw content which will trigger error handling  
                return r.content
                
        except Exception as e:
            print(f"[{dataset_name}] Download failed: {str(e)}")
            raise
    
    def process_dataframe(self, df, info):
        """Process the dataset into final form"""
        dataset_name = info['name']
        
        # Map X1-X8, Y1, Y2 columns to proper names for energy efficiency dataset
        if 'X1' in df.columns and 'Y2' in df.columns:
            column_mapping = {
                'X1': 'relative_compactness',
                'X2': 'surface_area', 
                'X3': 'wall_area',
                'X4': 'roof_area',
                'X5': 'overall_height',
                'X6': 'orientation',
                'X7': 'glazing_area',
                'X8': 'glazing_area_distribution',
                'Y1': 'heating_load',
                'Y2': 'cooling_load'
            }
            df = df.rename(columns=column_mapping)
            print(f"[{dataset_name}] Mapped X1-X8, Y1-Y2 to descriptive column names")
        
        # If dataframe has numeric column names, assign proper names
        elif all(isinstance(col, int) for col in df.columns):
            column_names = [
                'relative_compactness', 'surface_area', 'wall_area', 'roof_area',
                'overall_height', 'orientation', 'glazing_area', 'glazing_area_distribution',
                'heating_load', 'cooling_load'
            ]
            df.columns = column_names
            print(f"[{dataset_name}] Assigned column names")
        
        print(f"[{dataset_name}] DataFrame shape: {df.shape}")
        print(f"[{dataset_name}] Data types of columns:\n{df.dtypes}")
        print(f"[{dataset_name}] First 5 rows:\n{df.head().to_string()}")
        
        # Set the cooling_load column as the 'target' for regression if not already set
        if 'target' not in df.columns:
            if 'cooling_load' in df.columns:
                df['target'] = df['cooling_load']
                print(f"[{dataset_name}] Set 'cooling_load' as the target column")
            elif 'Y2' in df.columns:
                df['target'] = df['Y2']
                print(f"[{dataset_name}] Set 'Y2' (cooling_load) as the target column")
            else:
                # Use last column as target
                last_col = df.columns[-1]
                df['target'] = df[last_col]
                print(f"[{dataset_name}] Set last column '{last_col}' as the target column")
        
        # Check for missing values
        print(f"[{dataset_name}] Checking for missing values:")
        for col in df.columns:
            missing = df[col].isna().sum()
            print(f"  - {col}: {missing} missing")
        
        # Fill missing values if any
        if df.isna().any().any():
            print(f"[{dataset_name}] Filling missing values with column medians...")
            for col in df.columns:
                if df[col].isna().any():
                    df[col] = df[col].fillna(df[col].median())
        
        # Shuffle dataset
        print(f"[{dataset_name}] Shuffling the dataset randomly...")
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        print(f"[{dataset_name}] Dataset shuffled and indices reset.")
        
        # Final logging
        print(f"[{dataset_name}] Final DataFrame shape: {df.shape}")
        print(f"[{dataset_name}] Target summary:")
        print(f"  - Mean: {df['target'].mean():.2f}")
        print(f"  - Std: {df['target'].std():.2f}")
        print(f"  - Min: {df['target'].min():.2f}")
        print(f"  - Max: {df['target'].max():.2f}")
        print(f"[{dataset_name}] Sample of first 5 rows:\n{df.head().to_string()}")
        
        return df

# For testing
if __name__ == "__main__":
    dataset = EnergyEfficiencyDataset()
    df = dataset.get_data()
    print(f"Dataset loaded successfully with {len(df)} rows.") 
    # ------------------------------------------------------------------
    # Agent-aware feature engineering hooks (Energy Efficiency)
    # ------------------------------------------------------------------
    def get_feature_agent(self, provider: str = "GPT5"):
        return {"provider": provider, "name": "EnergyEfficiencyFeatureAgent", "version": "v1"}

    def _propose_agent_feature_plan(self, df: pd.DataFrame, agent) -> list:
        import numpy as np
        eps = 1e-6
        def has_all(cols):
            return all(c in df.columns for c in cols)
        plan = []

        # Building envelope features
        if has_all(["relative_compactness", "surface_area"]):
            plan.append({"name": "compactness_surface_ratio", "requires": ["relative_compactness", "surface_area"], 
                        "builder": lambda d: d["relative_compactness"] / (d["surface_area"] + eps)})
            plan.append({"name": "surface_per_compactness", "requires": ["relative_compactness", "surface_area"],
                        "builder": lambda d: d["surface_area"] * d["relative_compactness"]})
        
        # Wall/Roof interactions
        if has_all(["wall_area", "roof_area"]):
            plan.append({"name": "wall_roof_ratio", "requires": ["wall_area", "roof_area"],
                        "builder": lambda d: d["wall_area"] / (d["roof_area"] + eps)})
            plan.append({"name": "total_exterior_area", "requires": ["wall_area", "roof_area"],
                        "builder": lambda d: d["wall_area"] + d["roof_area"]})
        
        # Glazing features
        if has_all(["glazing_area", "wall_area"]):
            plan.append({"name": "glazing_wall_ratio", "requires": ["glazing_area", "wall_area"],
                        "builder": lambda d: d["glazing_area"] / (d["wall_area"] + eps)})
        
        if has_all(["glazing_area", "surface_area"]):
            plan.append({"name": "glazing_surface_ratio", "requires": ["glazing_area", "surface_area"],
                        "builder": lambda d: d["glazing_area"] / (d["surface_area"] + eps)})
        
        # Height-based features
        if "overall_height" in df.columns:
            plan.append({"name": "height_squared", "requires": ["overall_height"],
                        "builder": lambda d: d["overall_height"] ** 2})
            plan.append({"name": "height_log", "requires": ["overall_height"],
                        "builder": lambda d: np.log1p(d["overall_height"])})
        
        if has_all(["overall_height", "surface_area"]):
            plan.append({"name": "height_surface_ratio", "requires": ["overall_height", "surface_area"],
                        "builder": lambda d: d["overall_height"] / (d["surface_area"] + eps)})
        
        # Orientation features
        if "orientation" in df.columns:
            plan.append({"name": "is_north_facing", "requires": ["orientation"],
                        "builder": lambda d: (d["orientation"] == 2).astype(int)})
            plan.append({"name": "is_south_facing", "requires": ["orientation"],
                        "builder": lambda d: (d["orientation"] == 4).astype(int)})
            plan.append({"name": "is_east_west", "requires": ["orientation"],
                        "builder": lambda d: d["orientation"].isin([3, 5]).astype(int)})
        
        # Glazing distribution features
        if has_all(["glazing_area", "glazing_area_distribution"]):
            plan.append({"name": "glazing_concentration", "requires": ["glazing_area", "glazing_area_distribution"],
                        "builder": lambda d: d["glazing_area"] * (6 - d["glazing_area_distribution"]) / 5})
            plan.append({"name": "glazing_uniformity", "requires": ["glazing_area_distribution"],
                        "builder": lambda d: (d["glazing_area_distribution"] == 1).astype(int)})
        
        # Volume proxy features
        if has_all(["surface_area", "overall_height"]):
            plan.append({"name": "volume_proxy", "requires": ["surface_area", "overall_height"],
                        "builder": lambda d: d["surface_area"] * d["overall_height"] / 4})
        
        # Heat transfer features
        if has_all(["wall_area", "glazing_area", "roof_area"]):
            plan.append({"name": "weighted_heat_transfer_area", "requires": ["wall_area", "glazing_area", "roof_area"],
                        "builder": lambda d: d["wall_area"] + 3 * d["glazing_area"] + 0.5 * d["roof_area"]})
        
        # Aspect ratio features
        if has_all(["wall_area", "overall_height"]):
            plan.append({"name": "wall_height_ratio", "requires": ["wall_area", "overall_height"],
                        "builder": lambda d: d["wall_area"] / (d["overall_height"] + eps)})
        
        return plan

    @staticmethod
    def expand_features_on_dataframe(df: pd.DataFrame) -> (pd.DataFrame, list):
        self_like = EnergyEfficiencyDataset()
        agent = self_like.get_feature_agent(provider="GPT5")
        plan = self_like._propose_agent_feature_plan(df, agent)
        added = []
        for item in plan:
            name = item["name"]; requires = item["requires"]; builder = item["builder"]
            if name in df.columns:
                continue
            if all(col in df.columns for col in requires):
                try:
                    df[name] = builder(df); added.append(name)
                except Exception:
                    pass
        return df, added

    def get_data_gen(self, agent_provider: str = "GPT5", force: bool = False) -> pd.DataFrame:
        df = self.get_data()
        if isinstance(df, pd.DataFrame) and df.attrs.get("agent_expansion_applied") and not force:
            return df
        agent = self.get_feature_agent(provider=agent_provider)
        plan = self._propose_agent_feature_plan(df, agent)
        df, added = EnergyEfficiencyDataset.expand_features_on_dataframe(df)
        try:
            df.attrs["agent_expansion_applied"] = True
            df.attrs["agent_provider"] = agent_provider
            df.attrs["agent_expanded_features"] = added
        except Exception:
            pass
        return df
