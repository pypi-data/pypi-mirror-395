import pandas as pd
import numpy as np
import os
import tempfile
import sys
from pathlib import Path
# Ensure project root is on sys.path when running this file directly
try:
    # The repo root from this file is parents[6]
    ROOT = Path(__file__).resolve().parents[6]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
except Exception:
    pass
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class PipelineIntegrityDataset(BaseDatasetLoader):
    """
    Pipeline Integrity Monitoring Dataset (binary classification)
    Source: Kaggle - Pipeline Failure Prediction
    Target: failure_risk (0=safe, 1=at risk)
    
    This dataset contains pipeline sensor data and inspection results
    for predicting pipeline integrity issues and preventing failures.
    """
    
    def get_dataset_info(self):
        return {
            'name': 'PipelineIntegrityDataset',
            'source_id': 'kaggle:pipeline-integrity',
            'category': 'binary_classification',
            'description': 'Pipeline failure risk prediction from sensor and inspection data.',
            'source_url': 'https://www.kaggle.com/datasets/uciml/condition-monitoring-of-hydraulic-systems',
        }
    
    def download_dataset(self, info):
        """Download the pipeline integrity dataset from Kaggle"""
        print(f"[PipelineIntegrityDataset] Downloading from Kaggle...")
        
        try:
            import kaggle
            
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"[PipelineIntegrityDataset] Downloading to {temp_dir}")
                
                kaggle.api.dataset_download_files(
                    'uciml/condition-monitoring-of-hydraulic-systems',
                    path=temp_dir,
                    unzip=True
                )
                
                # Find CSV files
                csv_files = []
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith('.csv') or file.endswith('.txt'):
                            csv_files.append(os.path.join(root, file))
                
                if csv_files:
                    data_file = csv_files[0]
                    print(f"[PipelineIntegrityDataset] Reading: {os.path.basename(data_file)}")
                    df = pd.read_csv(data_file, nrows=10000)
                    print(f"[PipelineIntegrityDataset] Loaded {df.shape[0]} rows")
                    csv_data = df.to_csv(index=False)
                    return csv_data.encode('utf-8')
                
                raise FileNotFoundError("No data file found")
                
        except Exception as e:
            print(f"[PipelineIntegrityDataset] Download failed: {e}")
            print("[PipelineIntegrityDataset] Using sample pipeline integrity data...")
            
            # Create realistic pipeline integrity data
            np.random.seed(42)
            n_samples = 5000
            
            # Pipeline characteristics
            data = {}
            data['pipeline_age_years'] = np.random.gamma(3, 5, n_samples)
            data['pipeline_diameter_inches'] = np.random.choice([8, 12, 16, 20, 24, 30, 36, 42], n_samples)
            data['wall_thickness_mm'] = np.random.normal(12, 2, n_samples)
            data['material_grade'] = np.random.choice([1, 2, 3, 4, 5], n_samples)  # Material quality grades
            
            # Operating conditions
            data['operating_pressure_psi'] = np.random.normal(800, 150, n_samples)
            data['max_pressure_psi'] = data['operating_pressure_psi'] * np.random.uniform(1.2, 1.5, n_samples)
            data['flow_rate_mbpd'] = np.random.gamma(3, 50, n_samples)  # thousand barrels per day
            data['temperature_celsius'] = np.random.normal(40, 15, n_samples)
            
            # Corrosion indicators
            data['corrosion_rate_mpy'] = np.random.exponential(0.5, n_samples)  # mils per year
            data['ph_level'] = np.random.normal(7, 1, n_samples)
            data['water_content_ppm'] = np.random.exponential(100, n_samples)
            data['h2s_content_ppm'] = np.random.exponential(10, n_samples)
            data['co2_content_percent'] = np.random.exponential(0.5, n_samples)
            
            # Inspection data
            data['wall_loss_percent'] = np.random.beta(2, 20, n_samples) * 50
            data['pit_depth_mm'] = np.random.exponential(0.5, n_samples)
            data['crack_length_mm'] = np.random.exponential(0.1, n_samples)
            data['dent_depth_mm'] = np.random.exponential(0.2, n_samples)
            
            # Sensor readings
            data['vibration_amplitude'] = np.random.gamma(2, 0.5, n_samples)
            data['acoustic_emission_db'] = np.random.normal(60, 10, n_samples)
            data['strain_gauge_reading'] = np.random.normal(0, 0.001, n_samples)
            data['pressure_variance'] = np.random.exponential(5, n_samples)
            
            # Environmental factors
            data['soil_resistivity_ohm_m'] = np.random.gamma(3, 1000, n_samples)
            data['soil_moisture_percent'] = np.random.beta(3, 2, n_samples) * 100
            data['coating_condition_score'] = np.random.beta(5, 2, n_samples) * 10
            
            # Maintenance history
            data['days_since_inspection'] = np.random.exponential(180, n_samples)
            data['num_repairs'] = np.random.poisson(0.5, n_samples)
            data['cathodic_protection_voltage'] = np.random.normal(-0.85, 0.1, n_samples)
            
            # Calculate failure risk based on multiple factors
            risk_score = np.zeros(n_samples)
            
            # Age and wear factors
            risk_score += (data['pipeline_age_years'] > 20) * 0.15
            risk_score += (data['wall_loss_percent'] > 20) * 0.25
            risk_score += (data['wall_loss_percent'] > 30) * 0.25
            
            # Corrosion factors
            risk_score += (data['corrosion_rate_mpy'] > 1) * 0.2
            risk_score += (data['h2s_content_ppm'] > 50) * 0.15
            risk_score += (data['co2_content_percent'] > 2) * 0.1
            
            # Defect factors
            risk_score += (data['pit_depth_mm'] > 2) * 0.2
            risk_score += (data['crack_length_mm'] > 5) * 0.3
            risk_score += (data['dent_depth_mm'] > 3) * 0.15
            
            # Operating conditions
            risk_score += (data['operating_pressure_psi'] / data['max_pressure_psi'] > 0.8) * 0.15
            risk_score += (data['pressure_variance'] > 20) * 0.1
            
            # Environmental factors
            risk_score += (data['coating_condition_score'] < 5) * 0.15
            risk_score += (data['cathodic_protection_voltage'] > -0.7) * 0.2
            
            # Add randomness
            risk_score += np.random.normal(0, 0.1, n_samples)
            
            # Convert to binary
            data['target'] = (risk_score > 0.5).astype(int)
            
            df = pd.DataFrame(data)
            csv_data = df.to_csv(index=False)
            return csv_data.encode('utf-8')
    
    def process_dataframe(self, df, info):
        """Process the pipeline integrity dataset"""
        print(f"[PipelineIntegrityDataset] Raw shape: {df.shape}")
        print(f"[PipelineIntegrityDataset] Columns: {list(df.columns)[:10]}...")
        
        # Find target column
        target_col = None
        for col in ['failure', 'risk', 'integrity', 'condition', 'target']:
            if col in df.columns:
                target_col = col
                break
        
        if target_col and target_col != 'target':
            # Convert to binary if needed
            if df[target_col].dtype == 'object':
                # Map text values to binary
                df['target'] = df[target_col].apply(lambda x: 1 if str(x).lower() in ['fail', 'failure', 'risk', 'bad'] else 0)
            else:
                df['target'] = df[target_col]
            df = df.drop(target_col, axis=1)
        elif 'target' not in df.columns:
            # Create target from available features
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                # Use a combination of features to create risk score
                df['target'] = (df[numeric_cols].mean(axis=1) > df[numeric_cols].mean(axis=1).median()).astype(int)
            else:
                raise ValueError("No suitable target column found")
        
        # Remove non-numeric columns
        text_cols = ['timestamp', 'date', 'pipeline_id', 'location', 'operator']
        for col in text_cols:
            if col in df.columns:
                df = df.drop(col, axis=1)
        
        # Select numeric features
        feature_cols = []
        for col in df.columns:
            if col != 'target':
                df[col] = pd.to_numeric(df[col], errors='coerce')
                if df[col].notna().sum() > len(df) * 0.5:
                    feature_cols.append(col)
        
        # Limit features if too many
        if len(feature_cols) > 30:
            # Prioritize pipeline-specific features
            priority_features = ['pressure', 'corrosion', 'wall', 'thickness', 'age', 
                               'temperature', 'flow', 'vibration', 'crack', 'pit']
            
            selected_features = []
            for feat in priority_features:
                for col in feature_cols:
                    if feat in col.lower() and col not in selected_features:
                        selected_features.append(col)
            
            # Add remaining features up to limit
            for col in feature_cols:
                if col not in selected_features and len(selected_features) < 30:
                    selected_features.append(col)
            
            feature_cols = selected_features[:30]
        
        # Create final dataframe
        df = df[feature_cols + ['target']]
        
        # Handle missing values
        for col in df.columns:
            if df[col].isna().any():
                df[col] = df[col].fillna(df[col].median())
        
        # Ensure all numeric
        df = df.dropna()
        
        # Ensure target is binary
        df['target'] = df['target'].astype(int)
        df = df[df['target'].isin([0, 1])]
        
        # Balance classes if needed
        target_counts = df['target'].value_counts()
        if len(target_counts) == 2:
            minority_class = target_counts.idxmin()
            majority_class = target_counts.idxmax()
            
            if target_counts[minority_class] < target_counts[majority_class] * 0.1:
                # Undersample majority class
                n_minority = target_counts[minority_class]
                n_majority = min(n_minority * 5, target_counts[majority_class])
                
                df_minority = df[df['target'] == minority_class]
                df_majority = df[df['target'] == majority_class].sample(n=n_majority, random_state=42)
                df = pd.concat([df_minority, df_majority])
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[PipelineIntegrityDataset] Final shape: {df.shape}")
        print(f"[PipelineIntegrityDataset] Target distribution: {df['target'].value_counts().to_dict()}")
        print(f"[PipelineIntegrityDataset] Failure risk rate: {(df['target'] == 1).mean():.2%}")
        
        # Attach lightweight, non-invasive attrs to help downstream stages
        try:
            df.attrs["dataset_source"] = "PipelineIntegrityDataset"
            df.attrs["raw_feature_names"] = [c for c in df.columns if c != 'target']
            df.attrs["feature_expander"] = ("PipelineIntegrityDataset", "expand_features_on_dataframe")
        except Exception:
            pass
        
        return df

    # ------------------------------------------------------------------
    # Agent-aware feature engineering hooks (Pipeline Integrity)
    # ------------------------------------------------------------------
    def get_feature_agent(self, provider: str = "GPT5"):
        return {"provider": provider, "name": "PipelineIntegrityFeatureAgent", "version": "v1"}

    def _propose_agent_feature_plan(self, df: pd.DataFrame, agent) -> list:
        eps = 1e-6
        def has_all(cols):
            return all(c in df.columns for c in cols)

        plan = []

        # Pressure utilization and margin
        if has_all(["operating_pressure_psi", "max_pressure_psi"]):
            plan.append({
                "name": "pressure_utilization",
                "requires": ["operating_pressure_psi", "max_pressure_psi"],
                "builder": lambda d: d["operating_pressure_psi"] / (d["max_pressure_psi"] + eps),
            })
            plan.append({
                "name": "pressure_margin",
                "requires": ["operating_pressure_psi", "max_pressure_psi"],
                "builder": lambda d: (d["max_pressure_psi"] - d["operating_pressure_psi"]) / (d["max_pressure_psi"] + eps),
            })
            plan.append({
                "name": "pressure_safety_factor",
                "requires": ["operating_pressure_psi", "max_pressure_psi"],
                "builder": lambda d: d["max_pressure_psi"] / (d["operating_pressure_psi"] + eps),
            })

        # Geometry and flow ratios
        if has_all(["flow_rate_mbpd", "pipeline_diameter_inches"]):
            plan.append({
                "name": "flow_per_diameter",
                "requires": ["flow_rate_mbpd", "pipeline_diameter_inches"],
                "builder": lambda d: d["flow_rate_mbpd"] / (d["pipeline_diameter_inches"] + eps),
            })
        if has_all(["wall_thickness_mm", "pipeline_diameter_inches"]):
            plan.append({
                "name": "wall_to_diameter",
                "requires": ["wall_thickness_mm", "pipeline_diameter_inches"],
                "builder": lambda d: d["wall_thickness_mm"] / (d["pipeline_diameter_inches"] + eps),
            })

        # Corrosion and environment composite
        env_cols = [c for c in ["corrosion_rate_mpy", "water_content_ppm", "h2s_content_ppm", "co2_content_percent", "ph_level"] if c in df.columns]
        if has_all(env_cols) and len(env_cols) >= 3:
            def corrosion_env_index(d):
                cr = d.get("corrosion_rate_mpy") if "corrosion_rate_mpy" in d.columns else 0
                wc = d.get("water_content_ppm") if "water_content_ppm" in d.columns else 0
                h2s = d.get("h2s_content_ppm") if "h2s_content_ppm" in d.columns else 0
                co2 = d.get("co2_content_percent") if "co2_content_percent" in d.columns else 0
                ph = d.get("ph_level") if "ph_level" in d.columns else 7
                return cr + 0.0005 * wc + 0.02 * h2s + 0.3 * co2 + (7 - ph).clip(lower=0)
            plan.append({
                "name": "corrosion_env_index",
                "requires": env_cols,
                "builder": corrosion_env_index,
            })

        # Basic nonlinear transforms
        if has_all(["pipeline_age_years"]) and "age_squared":
            plan.append({
                "name": "age_squared",
                "requires": ["pipeline_age_years"],
                "builder": lambda d: (pd.to_numeric(d["pipeline_age_years"], errors="coerce").astype(float) ** 2),
            })
        if has_all(["operating_pressure_psi", "max_pressure_psi"]):
            plan.append({
                "name": "utilization_squared",
                "requires": ["operating_pressure_psi", "max_pressure_psi"],
                "builder": lambda d: (pd.to_numeric(d["operating_pressure_psi"], errors="coerce").astype(float) / (pd.to_numeric(d["max_pressure_psi"], errors="coerce").astype(float) + eps)) ** 2,
            })
        if has_all(["pipeline_age_years"]):
            plan.append({
                "name": "log1p_pipeline_age_years",
                "requires": ["pipeline_age_years"],
                "builder": lambda d: np.log1p(pd.to_numeric(d["pipeline_age_years"], errors="coerce").astype(float).clip(lower=0)),
            })
        if has_all(["corrosion_rate_mpy"]):
            plan.append({
                "name": "log1p_corrosion_rate_mpy",
                "requires": ["corrosion_rate_mpy"],
                "builder": lambda d: np.log1p(pd.to_numeric(d["corrosion_rate_mpy"], errors="coerce").astype(float).clip(lower=0)),
            })
        if has_all(["pressure_margin"]):
            plan.append({
                "name": "pressure_margin_sq",
                "requires": ["pressure_margin"],
                "builder": lambda d: (pd.to_numeric(d["pressure_margin"], errors="coerce").astype(float) ** 2),
            })

        # Defect severity composite
        defect_cols = [c for c in ["wall_loss_percent", "pit_depth_mm", "crack_length_mm", "dent_depth_mm"] if c in df.columns]
        if defect_cols:
            def defect_severity(d):
                wl = d.get("wall_loss_percent") if "wall_loss_percent" in d.columns else 0
                pit = d.get("pit_depth_mm") if "pit_depth_mm" in d.columns else 0
                crack = d.get("crack_length_mm") if "crack_length_mm" in d.columns else 0
                dent = d.get("dent_depth_mm") if "dent_depth_mm" in d.columns else 0
                return 0.04 * wl + 0.5 * pit + 0.3 * crack + 0.4 * dent
            plan.append({
                "name": "defect_severity",
                "requires": defect_cols,
                "builder": defect_severity,
            })

        # Protection deficit and coating-derived terms
        if has_all(["coating_condition_score", "cathodic_protection_voltage"]):
            plan.append({
                "name": "protection_deficit",
                "requires": ["coating_condition_score", "cathodic_protection_voltage"],
                "builder": lambda d: (10.0 - pd.to_numeric(d["coating_condition_score"], errors="coerce").astype(float)) + 10.0 * (pd.to_numeric(d["cathodic_protection_voltage"], errors="coerce").astype(float) + 0.75).clip(lower=0.0),
            })
            plan.append({
                "name": "protection_effectiveness",
                "requires": ["cathodic_protection_voltage", "coating_condition_score"],
                "builder": lambda d: ((pd.to_numeric(d["cathodic_protection_voltage"], errors="coerce").astype(float).abs() / 1.5) + (pd.to_numeric(d["coating_condition_score"], errors="coerce").astype(float) / 10.0)) / 2.0,
            })
            plan.append({
                "name": "prot_effect_sq",
                "requires": ["cathodic_protection_voltage", "coating_condition_score"],
                "builder": lambda d: (((pd.to_numeric(d["cathodic_protection_voltage"], errors="coerce").astype(float).abs() / 1.5) + (pd.to_numeric(d["coating_condition_score"], errors="coerce").astype(float) / 10.0)) / 2.0) ** 2,
            })
        if has_all(["coating_condition_score"]):
            plan.append({
                "name": "coating_deficit",
                "requires": ["coating_condition_score"],
                "builder": lambda d: ((10.0 - pd.to_numeric(d["coating_condition_score"], errors="coerce").astype(float)).clip(lower=0.0) / 10.0),
            })

        # Cathodic protection status flag
        if has_all(["cathodic_protection_voltage"]):
            plan.append({
                "name": "cathodic_out_of_spec",
                "requires": ["cathodic_protection_voltage"],
                "builder": lambda d: (d["cathodic_protection_voltage"] > -0.75).astype(int),
            })
            plan.append({
                "name": "cp_out_spec",
                "requires": ["cathodic_protection_voltage"],
                "builder": lambda d: (pd.to_numeric(d["cathodic_protection_voltage"], errors="coerce").astype(float) > -0.75).astype(int),
            })

        # Inspection recency bucket
        if has_all(["days_since_inspection"]):
            plan.append({
                "name": "inspection_recency_bucket",
                "requires": ["days_since_inspection"],
                "builder": lambda d: pd.cut(d["days_since_inspection"], bins=[-1, 30, 90, 180, 365, 10000], labels=[0,1,2,3,4]).astype("Int64").fillna(0),
            })

        # Vibrations under pressure variability
        if has_all(["vibration_amplitude", "pressure_variance"]):
            plan.append({
                "name": "vibration_pressure_interaction",
                "requires": ["vibration_amplitude", "pressure_variance"],
                "builder": lambda d: d["vibration_amplitude"] * d["pressure_variance"],
            })

        # Soil corrosion risk proxy
        soil_cols = [c for c in ["soil_resistivity_ohm_m", "soil_moisture_percent", "coating_condition_score"] if c in df.columns]
        if has_all(soil_cols) and len(soil_cols) == 3:
            plan.append({
                "name": "soil_corrosion_risk",
                "requires": soil_cols,
                "builder": lambda d: (1.0 / (d["soil_resistivity_ohm_m"] + eps)) * (d["soil_moisture_percent"] / 100.0) * (10.0 - d["coating_condition_score"]),
            })

        # Age x corrosion interaction
        if has_all(["pipeline_age_years", "corrosion_rate_mpy"]):
            plan.append({
                "name": "age_x_corrosion",
                "requires": ["pipeline_age_years", "corrosion_rate_mpy"],
                "builder": lambda d: d["pipeline_age_years"] * d["corrosion_rate_mpy"],
            })

        # Pressure shock indicator
        if has_all(["pressure_variance", "operating_pressure_psi"]):
            plan.append({
                "name": "pressure_variance_ratio",
                "requires": ["pressure_variance", "operating_pressure_psi"],
                "builder": lambda d: d["pressure_variance"] / (d["operating_pressure_psi"] + eps),
            })

        # Utilization × age
        if has_all(["pressure_utilization", "pipeline_age_years"]):
            plan.append({
                "name": "utilization_age_index",
                "requires": ["pressure_utilization", "pipeline_age_years"],
                "builder": lambda d: pd.to_numeric(d["pressure_utilization"], errors="coerce").astype(float) * pd.to_numeric(d["pipeline_age_years"], errors="coerce").astype(float),
            })

        # Coating/CP interactions
        if has_all(["coating_deficit", "pressure_utilization"]):
            plan.append({
                "name": "coating_deficit_util",
                "requires": ["coating_deficit", "pressure_utilization"],
                "builder": lambda d: pd.to_numeric(d["coating_deficit"], errors="coerce").astype(float) * pd.to_numeric(d["pressure_utilization"], errors="coerce").astype(float),
            })
        if has_all(["corrosion_q5", "coating_deficit"]):
            plan.append({
                "name": "q5_coating_deficit",
                "requires": ["corrosion_q5", "coating_deficit"],
                "builder": lambda d: pd.to_numeric(d["corrosion_q5"], errors="coerce").astype(float) * pd.to_numeric(d["coating_deficit"], errors="coerce").astype(float),
            })
        if has_all(["cp_out_spec", "pressure_utilization"]):
            plan.append({
                "name": "cp_out_util",
                "requires": ["cp_out_spec", "pressure_utilization"],
                "builder": lambda d: pd.to_numeric(d["cp_out_spec"], errors="coerce").astype(float) * pd.to_numeric(d["pressure_utilization"], errors="coerce").astype(float),
            })
            plan.append({
                "name": "cp_out_util_sq",
                "requires": ["cp_out_spec", "pressure_utilization"],
                "builder": lambda d: (pd.to_numeric(d["cp_out_spec"], errors="coerce").astype(float) * pd.to_numeric(d["pressure_utilization"], errors="coerce").astype(float)) ** 2,
            })
        if has_all(["cp_out_spec", "age_squared"]):
            plan.append({
                "name": "cp_out_age_sq",
                "requires": ["cp_out_spec", "age_squared"],
                "builder": lambda d: pd.to_numeric(d["cp_out_spec"], errors="coerce").astype(float) * pd.to_numeric(d["age_squared"], errors="coerce").astype(float),
            })

        # Age-protection interactions and sigmoids
        if has_all(["protection_deficit", "pipeline_age_years"]):
            plan.append({
                "name": "age_protection_deficit",
                "requires": ["protection_deficit", "pipeline_age_years"],
                "builder": lambda d: pd.to_numeric(d["protection_deficit"], errors="coerce").astype(float) * pd.to_numeric(d["pipeline_age_years"], errors="coerce").astype(float),
            })
            plan.append({
                "name": "log1p_age_prot_def",
                "requires": ["protection_deficit", "pipeline_age_years"],
                "builder": lambda d: np.log1p((pd.to_numeric(d["protection_deficit"], errors="coerce").astype(float) * pd.to_numeric(d["pipeline_age_years"], errors="coerce").astype(float)).clip(lower=0)),
            })
            plan.append({
                "name": "sqrt_age_prot_def",
                "requires": ["protection_deficit", "pipeline_age_years"],
                "builder": lambda d: (pd.to_numeric(d["protection_deficit"], errors="coerce").astype(float) * pd.to_numeric(d["pipeline_age_years"], errors="coerce").astype(float)).clip(lower=0) ** 0.5,
            })
            plan.append({
                "name": "age_prot_def_sq",
                "requires": ["protection_deficit", "pipeline_age_years"],
                "builder": lambda d: (pd.to_numeric(d["protection_deficit"], errors="coerce").astype(float) * pd.to_numeric(d["pipeline_age_years"], errors="coerce").astype(float)) ** 2,
            })
            plan.append({
                "name": "age_prot_def_cube",
                "requires": ["protection_deficit", "pipeline_age_years"],
                "builder": lambda d: (pd.to_numeric(d["protection_deficit"], errors="coerce").astype(float) * pd.to_numeric(d["pipeline_age_years"], errors="coerce").astype(float)) ** 3,
            })
            plan.append({
                "name": "sigmoid_age_prot",
                "requires": ["protection_deficit", "pipeline_age_years"],
                "builder": lambda d: 1.0 / (1.0 + np.exp(- (pd.to_numeric(d["protection_deficit"], errors="coerce").astype(float) * pd.to_numeric(d["pipeline_age_years"], errors="coerce").astype(float)) / 100.0)),
            })
        if has_all(["sigmoid_age_prot", "pressure_utilization"]):
            plan.append({
                "name": "sig_age_prot_util",
                "requires": ["sigmoid_age_prot", "pressure_utilization"],
                "builder": lambda d: pd.to_numeric(d["sigmoid_age_prot"], errors="coerce").astype(float) * pd.to_numeric(d["pressure_utilization"], errors="coerce").astype(float),
            })
        if has_all(["sqrt_age_prot_def", "cp_out_spec"]):
            plan.append({
                "name": "sqrt_age_cp_out",
                "requires": ["sqrt_age_prot_def", "cp_out_spec"],
                "builder": lambda d: pd.to_numeric(d["sqrt_age_prot_def"], errors="coerce").astype(float) * pd.to_numeric(d["cp_out_spec"], errors="coerce").astype(float),
            })
        if has_all(["cp_out_spec", "sigmoid_age_prot"]):
            plan.append({
                "name": "cp_out_sig_age",
                "requires": ["cp_out_spec", "sigmoid_age_prot"],
                "builder": lambda d: pd.to_numeric(d["cp_out_spec"], errors="coerce").astype(float) * pd.to_numeric(d["sigmoid_age_prot"], errors="coerce").astype(float),
            })

        # Corrosion quantiles and polynomials
        if has_all(["log1p_corrosion_rate_mpy"]) or has_all(["corrosion_rate_mpy"]):
            plan.append({
                "name": "corrosion_q5",
                "requires": [c for c in ["log1p_corrosion_rate_mpy", "corrosion_rate_mpy"] if c in df.columns],
                "builder": lambda d: pd.qcut((d["log1p_corrosion_rate_mpy"] if "log1p_corrosion_rate_mpy" in d.columns else pd.to_numeric(d["corrosion_rate_mpy"], errors="coerce")).rank(method="average"), 5, labels=False, duplicates="drop").astype("Int64").fillna(0),
            })
        if has_all(["corrosion_q5"]):
            plan.append({
                "name": "corrosion_q5_sq",
                "requires": ["corrosion_q5"],
                "builder": lambda d: (pd.to_numeric(d["corrosion_q5"], errors="coerce").astype(float) ** 2),
            })
            plan.append({
                "name": "sqrt_corrosion_q5",
                "requires": ["corrosion_q5"],
                "builder": lambda d: (pd.to_numeric(d["corrosion_q5"], errors="coerce").astype(float).clip(lower=0) ** 0.5),
            })
            plan.append({
                "name": "corrosion_q5_cube",
                "requires": ["corrosion_q5"],
                "builder": lambda d: (pd.to_numeric(d["corrosion_q5"], errors="coerce").astype(float) ** 3),
            })
            plan.append({
                "name": "corrosion_q5_pow4",
                "requires": ["corrosion_q5"],
                "builder": lambda d: (pd.to_numeric(d["corrosion_q5"], errors="coerce").astype(float) ** 4),
            })
        if has_all(["corrosion_q5_sq", "sqrt_corrosion_q5"]):
            plan.append({
                "name": "q5_sq_sqrt",
                "requires": ["corrosion_q5_sq", "sqrt_corrosion_q5"],
                "builder": lambda d: pd.to_numeric(d["corrosion_q5_sq"], errors="coerce").astype(float) * pd.to_numeric(d["sqrt_corrosion_q5"], errors="coerce").astype(float),
            })
        if has_all(["q5_sq_sqrt", "pressure_utilization"]):
            plan.append({
                "name": "q5_sq_sqrt_util",
                "requires": ["q5_sq_sqrt", "pressure_utilization"],
                "builder": lambda d: pd.to_numeric(d["q5_sq_sqrt"], errors="coerce").astype(float) * pd.to_numeric(d["pressure_utilization"], errors="coerce").astype(float),
            })
        if has_all(["corrosion_q5_pow4", "pressure_utilization"]):
            plan.append({
                "name": "q5_pow4_util",
                "requires": ["corrosion_q5_pow4", "pressure_utilization"],
                "builder": lambda d: pd.to_numeric(d["corrosion_q5_pow4"], errors="coerce").astype(float) * pd.to_numeric(d["pressure_utilization"], errors="coerce").astype(float),
            })
        if has_all(["corrosion_q5_cube", "pressure_utilization"]):
            plan.append({
                "name": "q5_cube_util",
                "requires": ["corrosion_q5_cube", "pressure_utilization"],
                "builder": lambda d: pd.to_numeric(d["corrosion_q5_cube"], errors="coerce").astype(float) * pd.to_numeric(d["pressure_utilization"], errors="coerce").astype(float),
            })
        if has_all(["corrosion_q5_sq"]):
            plan.append({
                "name": "log1p_q5_sq",
                "requires": ["corrosion_q5_sq"],
                "builder": lambda d: np.log1p(pd.to_numeric(d["corrosion_q5_sq"], errors="coerce").astype(float).clip(lower=0)),
            })
        if has_all(["q5_sq_sqrt"]):
            plan.append({
                "name": "log1p_q5_sq_sqrt",
                "requires": ["q5_sq_sqrt"],
                "builder": lambda d: np.log1p(pd.to_numeric(d["q5_sq_sqrt"], errors="coerce").astype(float).clip(lower=0)),
            })
        if has_all(["corrosion_q5_cube", "corrosion_q5_sq"]):
            plan.append({
                "name": "q5_cube_sq_ratio",
                "requires": ["corrosion_q5_cube", "corrosion_q5_sq"],
                "builder": lambda d: pd.to_numeric(d["corrosion_q5_cube"], errors="coerce").astype(float) / (pd.to_numeric(d["corrosion_q5_sq"], errors="coerce").astype(float) + 0.1),
            })
        if has_all(["corrosion_q5", "cathodic_protection_voltage"]):
            plan.append({
                "name": "q5_cp_voltage",
                "requires": ["corrosion_q5", "cathodic_protection_voltage"],
                "builder": lambda d: pd.to_numeric(d["corrosion_q5"], errors="coerce").astype(float) * pd.to_numeric(d["cathodic_protection_voltage"], errors="coerce").astype(float),
            })
        if has_all(["corrosion_q5"]):
            plan.append({
                "name": "exp_neg_q5",
                "requires": ["corrosion_q5"],
                "builder": lambda d: np.exp(-pd.to_numeric(d["corrosion_q5"], errors="coerce").astype(float) / 5.0),
            })
        if has_all(["corrosion_q5_pow4", "age_protection_deficit"]):
            plan.append({
                "name": "q5_pow4_age_prot",
                "requires": ["corrosion_q5_pow4", "age_protection_deficit"],
                "builder": lambda d: pd.to_numeric(d["corrosion_q5_pow4"], errors="coerce").astype(float) * pd.to_numeric(d["age_protection_deficit"], errors="coerce").astype(float),
            })
        if has_all(["sqrt_corrosion_q5", "age_protection_deficit"]):
            plan.append({
                "name": "sqrt_q5_age_prot",
                "requires": ["sqrt_corrosion_q5", "age_protection_deficit"],
                "builder": lambda d: pd.to_numeric(d["sqrt_corrosion_q5"], errors="coerce").astype(float) * pd.to_numeric(d["age_protection_deficit"], errors="coerce").astype(float),
            })
        if has_all(["sqrt_corrosion_q5", "sigmoid_age_prot"]):
            plan.append({
                "name": "q5_sqrt_sig_age",
                "requires": ["sqrt_corrosion_q5", "sigmoid_age_prot"],
                "builder": lambda d: pd.to_numeric(d["sqrt_corrosion_q5"], errors="coerce").astype(float) * pd.to_numeric(d["sigmoid_age_prot"], errors="coerce").astype(float),
            })
        if has_all(["corrosion_q5_pow4", "sigmoid_age_prot"]):
            plan.append({
                "name": "q5_pow4_sig_age",
                "requires": ["corrosion_q5_pow4", "sigmoid_age_prot"],
                "builder": lambda d: pd.to_numeric(d["corrosion_q5_pow4"], errors="coerce").astype(float) * pd.to_numeric(d["sigmoid_age_prot"], errors="coerce").astype(float),
            })
        if has_all(["age_squared", "pressure_utilization"]):
            plan.append({
                "name": "age_sq_util",
                "requires": ["age_squared", "pressure_utilization"],
                "builder": lambda d: pd.to_numeric(d["age_squared"], errors="coerce").astype(float) * pd.to_numeric(d["pressure_utilization"], errors="coerce").astype(float),
            })
        if has_all(["protection_deficit", "pipeline_age_years", "corrosion_rate_mpy"]):
            plan.append({
                "name": "age_prot_corr",
                "requires": ["protection_deficit", "pipeline_age_years", "corrosion_rate_mpy"],
                "builder": lambda d: (pd.to_numeric(d["protection_deficit"], errors="coerce").astype(float) * pd.to_numeric(d["pipeline_age_years"], errors="coerce").astype(float)) * pd.to_numeric(d["corrosion_rate_mpy"], errors="coerce").astype(float),
            })

        return plan

    @staticmethod
    def expand_features_on_dataframe(df: pd.DataFrame) -> (pd.DataFrame, list):
        self_like = PipelineIntegrityDataset()
        agent = self_like.get_feature_agent(provider="GPT5")
        plan = self_like._propose_agent_feature_plan(df, agent)
        added = []
        for item in plan:
            name = item["name"]
            requires = item["requires"]
            builder = item["builder"]
            if name in df.columns:
                continue
            if all(col in df.columns for col in requires):
                try:
                    df[name] = builder(df)
                    added.append(name)
                except Exception:
                    pass
        return df, added

    def get_data_gen(self, agent_provider: str = "GPT5", force: bool = False) -> pd.DataFrame:
        df = self.get_data()
        if isinstance(df, pd.DataFrame) and df.attrs.get("agent_expansion_applied") and not force:
            return df
        agent = self.get_feature_agent(provider=agent_provider)
        plan = self._propose_agent_feature_plan(df, agent)
        df, added = self.expand_features_on_dataframe(df)
        try:
            df.attrs["agent_expansion_applied"] = True
            df.attrs["agent_provider"] = agent_provider
            df.attrs["agent_expanded_features"] = added
        except Exception:
            pass
        return df

if __name__ == "__main__":
    dataset = PipelineIntegrityDataset()
    df = dataset.get_data()
    print(f"Loaded PipelineIntegrityDataset: {df.shape}")
    print(df.head())

    # Expanded view without re-download
    df_exp = df.copy(deep=True)
    df_exp, added = PipelineIntegrityDataset.expand_features_on_dataframe(df_exp)
    try:
        df_exp.attrs["agent_expansion_applied"] = True
        df_exp.attrs["agent_provider"] = "GPT5"
        df_exp.attrs["agent_expanded_features"] = list(added)
    except Exception:
        pass

    # 5-fold CatBoost AUC comparison
    try:
        from sklearn.model_selection import StratifiedKFold
        from sklearn.metrics import roc_auc_score
        from catboost import CatBoostClassifier
        from app.seed_data.Generative.shared.stages.transforms.expanders.AgentFeatureExpander import AgentFeatureExpander

        X_base = df.drop(columns=["target"])
        y = df["target"]
        X_exp = df_exp.drop(columns=["target"])

        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        aucs_base = []
        aucs_exp = []

        print("\nBaseline (no expander) 5-fold AUCs:")
        for fold_idx, (train_idx, test_idx) in enumerate(skf.split(X_base, y)):
            # Baseline
            Xtr = X_base.iloc[train_idx]
            Xte = X_base.iloc[test_idx]
            ytr = y.iloc[train_idx]
            yte = y.iloc[test_idx]

            model = CatBoostClassifier(verbose=False, depth=6, learning_rate=0.1, iterations=300, loss_function="Logloss", eval_metric="AUC", random_seed=42)
            model.fit(Xtr, ytr)
            p = model.predict_proba(Xte)[:, 1]
            auc = roc_auc_score(yte, p)
            aucs_base.append(auc)
            print(f"Fold {fold_idx}: AUC={auc:.6f}")

        print("\nAgent-expanded 5-fold AUCs:")
        # Recreate splitter to keep the same folds
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        for fold_idx, (train_idx, test_idx) in enumerate(skf.split(X_exp, y)):
            Xtr2 = X_exp.iloc[train_idx].copy()
            Xte2 = X_exp.iloc[test_idx].copy()
            ytr2 = y.iloc[train_idx]
            yte2 = y.iloc[test_idx]

            expander = AgentFeatureExpander(prefer_dataset="PipelineIntegrityDataset")
            Xtr2 = expander.fit_transform(Xtr2, ytr2)
            Xte2 = expander.transform(Xte2)

            model2 = CatBoostClassifier(verbose=False, depth=6, learning_rate=0.1, iterations=300, loss_function="Logloss", eval_metric="AUC", random_seed=42)
            model2.fit(Xtr2, ytr2)
            p2 = model2.predict_proba(Xte2)[:, 1]
            auc2 = roc_auc_score(yte2, p2)
            aucs_exp.append(auc2)
            print(f"Fold {fold_idx}: AUC={auc2:.6f}")

        print({
            "baseline_auc_mean": float(np.mean(aucs_base)),
            "baseline_auc_std": float(np.std(aucs_base)),
            "expanded_auc_mean": float(np.mean(aucs_exp)),
            "expanded_auc_std": float(np.std(aucs_exp)),
            "folds": len(aucs_base),
            "added_features": len(added),
        })
    except Exception as e:
        print(f"[PipelineIntegrityDataset] CV run skipped due to: {e}")