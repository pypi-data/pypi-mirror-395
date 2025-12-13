import pandas as pd
import requests
import io
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class StudentPerformanceDataset(BaseDatasetLoader):
    """Student Performance dataset from UCI ML Repository for regression."""

    def get_dataset_info(self):
        return {
            'name': 'StudentPerformanceDataset',
            'source_id': 'uci:student_performance',
            'category': 'regression',
            'description': 'Student Performance dataset: predict final grade from student attributes.',
            'target_column': 'G3'
        }
    
    def download_dataset(self, info):
        dataset_name = info['name']
        # Math performance dataset
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00320/student.zip"
        print(f"[{dataset_name}] Downloading from {url}")
        
        try:
            response = requests.get(url, timeout=30)
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}")
            
            # Extract math dataset from zip
            import zipfile
            from io import BytesIO
            
            with zipfile.ZipFile(BytesIO(response.content)) as z:
                # Read the math dataset
                with z.open('student-mat.csv') as f:
                    return f.read()
        except Exception as e:
            print(f"[{dataset_name}] Download failed: {e}")
            # Fallback using direct CSV link
            try:
                fallback_url = "https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/student-mat.csv"
                response = requests.get(fallback_url, timeout=30)
                if response.status_code == 200:
                    return response.content
            except:
                pass
            raise
    
    def process_dataframe(self, df, info):
        dataset_name = info['name']
        
        # Handle semicolon separator if needed
        if df.shape[1] == 1:
            text = '\n'.join(df.iloc[:, 0].astype(str))
            df = pd.read_csv(io.StringIO(text), sep=';')
        
        # Convert categorical variables to numeric using label encoding
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            df[col] = pd.Categorical(df[col]).codes
        
        # Determine target column – prefer 'G3', otherwise default to last column
        target_source_col = 'G3' if 'G3' in df.columns else df.columns[-1]

        # Ensure we have a unified 'target' column and remove the source if different
        if 'target' not in df.columns:
            df['target'] = df[target_source_col]
            if target_source_col != 'target':
                df = df.drop(target_source_col, axis=1)
        
        # Ensure target is last column
        if 'target' in df.columns:
            cols = [col for col in df.columns if col != 'target'] + ['target']
            df = df[cols]
        
        # Handle missing values
        df = df.fillna(df.median())
        
        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        
        print(f"[{dataset_name}] Final shape: {df.shape}, Target range: {df['target'].min():.1f}-{df['target'].max():.1f}")
        return df 

if __name__ == "__main__":
    ds = StudentPerformanceDataset()
    frame = ds.get_data()
    print(frame.head()) 
    # ------------------------------------------------------------------
    # Agent-aware feature engineering hooks (Student Performance)
    # ------------------------------------------------------------------
    def get_feature_agent(self, provider: str = "GPT5"):
        return {"provider": provider, "name": "StudentPerformanceFeatureAgent", "version": "v1"}

    def _propose_agent_feature_plan(self, df: pd.DataFrame, agent) -> list:
        import numpy as np
        eps = 1e-6
        def has_all(cols):
            return all(c in df.columns for c in cols)
        plan = []

        # Study time features
        if has_all(["studytime", "freetime"]):
            plan.append({"name": "study_free_ratio", "requires": ["studytime", "freetime"],
                        "builder": lambda d: d["studytime"] / (d["freetime"] + eps)})
            plan.append({"name": "total_time_commitment", "requires": ["studytime", "freetime"],
                        "builder": lambda d: d["studytime"] + d["freetime"]})
        
        # Family education features
        if has_all(["Medu", "Fedu"]):
            plan.append({"name": "parent_edu_max", "requires": ["Medu", "Fedu"],
                        "builder": lambda d: np.maximum(d["Medu"], d["Fedu"])})
            plan.append({"name": "parent_edu_avg", "requires": ["Medu", "Fedu"],
                        "builder": lambda d: (d["Medu"] + d["Fedu"]) / 2})
            plan.append({"name": "parent_edu_diff", "requires": ["Medu", "Fedu"],
                        "builder": lambda d: np.abs(d["Medu"] - d["Fedu"])})
        
        # Health and absence interaction
        if has_all(["health", "absences"]):
            plan.append({"name": "health_absence_score", "requires": ["health", "absences"],
                        "builder": lambda d: d["health"] / (1 + d["absences"])})
            plan.append({"name": "poor_health_absent", "requires": ["health", "absences"],
                        "builder": lambda d: (d["health"] <= 2) * d["absences"]})
        
        # Social features
        if has_all(["goout", "Dalc", "Walc"]):
            plan.append({"name": "social_drinking_index", "requires": ["goout", "Dalc", "Walc"],
                        "builder": lambda d: d["goout"] * (d["Dalc"] + d["Walc"]) / 2})
        
        # Academic support
        if has_all(["schoolsup", "famsup", "paid"]):
            plan.append({"name": "total_support", "requires": ["schoolsup", "famsup", "paid"],
                        "builder": lambda d: d["schoolsup"] + d["famsup"] + d["paid"]})
        
        # Travel time and study efficiency
        if has_all(["traveltime", "studytime"]):
            plan.append({"name": "study_efficiency", "requires": ["traveltime", "studytime"],
                        "builder": lambda d: d["studytime"] / (d["traveltime"] + 1)})
        
        # Failure features
        if "failures" in df.columns:
            plan.append({"name": "has_failed", "requires": ["failures"],
                        "builder": lambda d: (d["failures"] > 0).astype(int)})
            plan.append({"name": "multiple_failures", "requires": ["failures"],
                        "builder": lambda d: (d["failures"] >= 2).astype(int)})
        
        # Age-related features
        if "age" in df.columns:
            plan.append({"name": "is_adult", "requires": ["age"],
                        "builder": lambda d: (d["age"] >= 18).astype(int)})
            plan.append({"name": "age_deviation", "requires": ["age"],
                        "builder": lambda d: np.abs(d["age"] - 16)})  # 16 is typical age
        
        # Internet and study relationship
        if has_all(["internet", "studytime"]):
            plan.append({"name": "internet_study_product", "requires": ["internet", "studytime"],
                        "builder": lambda d: d["internet"] * d["studytime"]})
        
        # Relationship status and going out
        if has_all(["romantic", "goout"]):
            plan.append({"name": "romantic_social", "requires": ["romantic", "goout"],
                        "builder": lambda d: d["romantic"] * d["goout"]})
        
        # Family size and support
        if has_all(["famsize", "famsup"]):
            plan.append({"name": "family_support_indicator", "requires": ["famsize", "famsup"],
                        "builder": lambda d: (d["famsize"] == 1) * d["famsup"]})  # GT3=1, LE3=0 typically
        
        # Extra activities impact
        if has_all(["activities", "studytime", "freetime"]):
            plan.append({"name": "activity_time_impact", "requires": ["activities", "studytime", "freetime"],
                        "builder": lambda d: d["activities"] * (5 - d["studytime"] - d["freetime"])})
        
        return plan

    @staticmethod
    def expand_features_on_dataframe(df: pd.DataFrame) -> (pd.DataFrame, list):
        self_like = StudentPerformanceDataset()
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
        df, added = StudentPerformanceDataset.expand_features_on_dataframe(df)
        try:
            df.attrs["agent_expansion_applied"] = True
            df.attrs["agent_provider"] = agent_provider
            df.attrs["agent_expanded_features"] = added
        except Exception:
            pass
        return df
