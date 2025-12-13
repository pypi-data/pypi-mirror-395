import pandas as pd
import numpy as np
import os
import tempfile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader


class HospitalReadmissionsAugmentedDataset(BaseDatasetLoader):
    """
    Hospital Readmissions Dataset with engineered features (binary classification)

    This loader mirrors the base HospitalReadmissionsDataset source and processing,
    but adds a set of domain-inspired, hard-coded derived features prior to the
    target column to improve model signal.
    """

    def get_dataset_info(self):
        return {
            'name': 'HospitalReadmissionsAugmentedDataset',
            'source_id': 'kaggle:hospital-readmissions|augmented_v1',
            'category': 'binary_classification',
            'description': 'Hospital readmissions dataset with engineered features.',
            'source_url': 'https://www.kaggle.com/datasets/dubradave/hospital-readmissions',
        }

    def download_dataset(self, info):
        """Download the hospital readmissions dataset from Kaggle (same as base)."""
        print(f"[HospitalReadmissionsAugmentedDataset] Downloading from Kaggle...")

        try:
            import kaggle

            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"[HospitalReadmissionsAugmentedDataset] Downloading to {temp_dir}")

                kaggle.api.dataset_download_files(
                    'dubradave/hospital-readmissions',
                    path=temp_dir,
                    unzip=True
                )

                # Find CSV file
                csv_files = []
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith('.csv'):
                            csv_files.append(os.path.join(root, file))

                if not csv_files:
                    raise FileNotFoundError("No CSV file found")

                data_file = csv_files[0]
                print(f"[HospitalReadmissionsAugmentedDataset] Reading: {os.path.basename(data_file)}")

                df = pd.read_csv(data_file)
                print(f"[HospitalReadmissionsAugmentedDataset] Loaded {df.shape[0]} rows, {df.shape[1]} columns")
                return df

        except Exception as e:
            print(f"[HospitalReadmissionsAugmentedDataset] Download failed: {e}")
            print("[HospitalReadmissionsAugmentedDataset] Using sample data...")

            # Create sample data (aligned with base for comparability)
            np.random.seed(42)
            n_samples = 10000

            data = {
                'time_in_hospital': np.random.randint(1, 15, n_samples),
                'n_lab_procedures': np.random.randint(1, 120, n_samples),
                'n_procedures': np.random.randint(0, 7, n_samples),
                'n_medications': np.random.randint(1, 75, n_samples),
                'n_outpatient': np.random.randint(0, 40, n_samples),
                'n_inpatient': np.random.randint(0, 20, n_samples),
                'n_emergency': np.random.randint(0, 70, n_samples),
                'medical_specialty': np.random.choice(['Cardiology', 'InternalMedicine', 'Surgery',
                                                       'Family/GeneralPractice', 'Emergency/Trauma'], n_samples),
                'diag_1': np.random.randint(1, 1000, n_samples),
                'diag_2': np.random.randint(1, 1000, n_samples),
                'diag_3': np.random.randint(1, 1000, n_samples),
                'glucose_test': np.random.choice(['no', 'normal', 'abnormal'], n_samples, p=[0.8, 0.1, 0.1]),
                'A1Ctest': np.random.choice(['no', 'normal', 'abnormal'], n_samples, p=[0.8, 0.1, 0.1]),
                'change': np.random.choice(['no', 'yes'], n_samples, p=[0.5, 0.5]),
                'diabetes_med': np.random.choice(['no', 'yes'], n_samples, p=[0.3, 0.7]),
                'readmitted': np.random.choice(['NO', '<30'], n_samples, p=[0.88, 0.12])
            }

            df = pd.DataFrame(data)
            return df

    def process_dataframe(self, df, info):
        """Process dataset and add engineered features before the target column."""
        print(f"[HospitalReadmissionsAugmentedDataset] Raw shape: {df.shape}")

        # Create binary target
        if 'readmitted' in df.columns:
            df['target'] = (df['readmitted'] == '<30').astype(int)
        else:
            # Fallback (should be rare when Kaggle is available)
            df['target'] = np.random.choice([0, 1], len(df), p=[0.88, 0.12])

        # Preserve some raw categorical strings for engineered booleans
        raw_change = df['change'] if 'change' in df.columns else None
        raw_diabetes_med = df['diabetes_med'] if 'diabetes_med' in df.columns else None
        raw_glucose = df['glucose_test'] if 'glucose_test' in df.columns else None
        raw_a1c = df['A1Ctest'] if 'A1Ctest' in df.columns else None

        # Base numeric features
        numeric_cols = [
            'time_in_hospital', 'n_lab_procedures', 'n_procedures',
            'n_medications', 'n_outpatient', 'n_inpatient', 'n_emergency'
        ]
        available_numeric = [col for col in numeric_cols if col in df.columns]

        # Diagnosis numeric handling
        diag_cols = ['diag_1', 'diag_2', 'diag_3']
        for col in diag_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                available_numeric.append(col)

        # Engineered features (safe divisions)
        def _safe_div(a, b):
            return a / np.where(b == 0, 1, b)

        # Visits aggregate and ratios
        if all(c in df.columns for c in ['n_outpatient', 'n_inpatient', 'n_emergency']):
            df['total_visits'] = df['n_outpatient'] + df['n_inpatient'] + df['n_emergency']
            df['inpatient_ratio'] = _safe_div(df['n_inpatient'], df['total_visits'])
            df['emergency_ratio'] = _safe_div(df['n_emergency'], df['total_visits'])
            df['outpatient_ratio'] = _safe_div(df['n_outpatient'], df['total_visits'])
            available_numeric += ['total_visits', 'inpatient_ratio', 'emergency_ratio', 'outpatient_ratio']

        # Utilization per day
        if 'time_in_hospital' in df.columns:
            if 'n_lab_procedures' in df.columns:
                df['labs_per_day'] = _safe_div(df['n_lab_procedures'], df['time_in_hospital'])
                available_numeric.append('labs_per_day')
            if 'n_medications' in df.columns:
                df['meds_per_day'] = _safe_div(df['n_medications'], df['time_in_hospital'])
                available_numeric.append('meds_per_day')
            if 'n_procedures' in df.columns:
                df['procedures_per_day'] = _safe_div(df['n_procedures'], df['time_in_hospital'])
                available_numeric.append('procedures_per_day')
            if all(c in df.columns for c in ['n_lab_procedures', 'n_procedures', 'n_medications']):
                df['resource_intensity'] = _safe_div(
                    df['n_lab_procedures'] + 3 * df['n_procedures'] + 0.5 * df['n_medications'],
                    df['time_in_hospital']
                )
                available_numeric.append('resource_intensity')

        # Diagnosis summary stats
        have_diags = [c for c in diag_cols if c in df.columns]
        if len(have_diags) >= 1:
            df['diag_max'] = df[have_diags].max(axis=1)
            df['diag_min'] = df[have_diags].min(axis=1)
            if len(have_diags) > 1:
                df['diag_mean'] = df[have_diags].mean(axis=1)
                available_numeric += ['diag_max', 'diag_min', 'diag_mean']
            else:
                available_numeric += ['diag_max', 'diag_min']

        # Boolean indicators from raw categorical values (prior to encoding)
        if raw_change is not None:
            df['change_yes'] = (raw_change.astype(str) == 'yes').astype(int)
            available_numeric.append('change_yes')
        if raw_diabetes_med is not None:
            df['diabetes_med_yes'] = (raw_diabetes_med.astype(str) == 'yes').astype(int)
            available_numeric.append('diabetes_med_yes')
        if raw_glucose is not None:
            df['glucose_abnormal'] = (raw_glucose.astype(str) == 'abnormal').astype(int)
            available_numeric.append('glucose_abnormal')
        if raw_a1c is not None:
            df['a1c_abnormal'] = (raw_a1c.astype(str) == 'abnormal').astype(int)
            available_numeric.append('a1c_abnormal')

        # Categorical encoding (add codes as features too)
        categorical_cols = ['medical_specialty', 'glucose_test', 'A1Ctest', 'change', 'diabetes_med']
        for col in categorical_cols:
            if col in df.columns:
                df[col] = pd.Categorical(df[col]).codes
                available_numeric.append(col)

        # Final column ordering: engineered/base features first, then target
        # Keep only available numeric columns and target
        keep_cols = [c for c in available_numeric if c in df.columns]
        # Remove duplicates while preserving order
        seen = set()
        ordered_unique = []
        for c in keep_cols:
            if c not in seen:
                ordered_unique.append(c)
                seen.add(c)

        df = df[ordered_unique + ['target']]

        # Clean numeric types and drop missing
        for col in df.columns:
            if col != 'target':
                df[col] = pd.to_numeric(df[col], errors='coerce')
                if df[col].dtype == 'int8':
                    df[col] = df[col].astype('int64')

        df = df.dropna()

        # Shuffle rows for downstream modeling reproducibility
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)

        print(f"[HospitalReadmissionsAugmentedDataset] Final shape: {df.shape}")
        print(f"[HospitalReadmissionsAugmentedDataset] Target distribution: {df['target'].value_counts().to_dict()}")

        return df


if __name__ == "__main__":
    dataset = HospitalReadmissionsAugmentedDataset()
    df = dataset.get_data()
    print(f"Loaded HospitalReadmissionsAugmentedDataset: {df.shape}")
    print(df.head())


