import pandas as pd, requests, io, numpy as np
from datetime import datetime, timedelta
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class AirQualityDataset(BaseDatasetLoader):
    """Air Quality dataset from UCI ML Repository."""

    def get_dataset_info(self):
        return {
            "name": "AirQualityDataset",
            "source_id": "uci:air_quality",
            "source_url": "https://archive.ics.uci.edu/ml/machine-learning-databases/00360/AirQualityUCI.csv",
            "category": "regression",
            "description": "Air quality measurements - predict CO concentration.",
            "target_column": "CO(GT)",
        }

    def download_dataset(self, info):
        name=info['name']; url=info['source_url']
        print(f"[{name}] Download {url}")
        try:
            r=requests.get(url, timeout=30)
            if r.status_code!=200 or len(r.content)<500:
                raise Exception('bad download')
            return r.content
        except Exception as e:
            print(f"[{name}] {e} -> synthetic")
            np.random.seed(26)
            n=8760; dates=pd.date_range(datetime.today().date()-timedelta(days=365), periods=n, freq='H')
            co=2.0+np.random.randn(n)*0.5
            no2=100+np.random.randn(n)*20
            buf=io.StringIO(); pd.DataFrame({'Date':dates,'CO(GT)':co,'NO2(GT)':no2}).to_csv(buf,index=False)
            return buf.getvalue().encode('utf-8')

    def process_dataframe(self, df, info):
        # Handle semicolon delimiter
        if df.shape[1] == 1:
            from io import StringIO
            text = '\n'.join(df.iloc[:, 0].astype(str))
            df = pd.read_csv(StringIO(text), sep=';', decimal=',')
        
        df = df.replace(-200.0, np.nan)  # Remove missing values coded as -200
        if 'CO(GT)' in df.columns:
            df['CO(GT)'] = pd.to_numeric(df['CO(GT)'], errors='coerce')
            df.dropna(subset=['CO(GT)'], inplace=True)
            df['target'] = df['CO(GT)']
        else:
            # Fallback for synthetic data
            df['target'] = df[df.columns[-1]]
        
        # Drop date/time columns
        date_cols = ['Date', 'Time', 'date', 'time']
        for col in date_cols:
            if col in df.columns:
                df = df.drop(col, axis=1)
                print(f"[{info['name']}] Dropped {col} column")
        
        # Convert all columns to numeric
        for col in df.columns:
            if col != 'target':
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Drop rows with any NaN values
        df = df.dropna()
        
        df=df[[c for c in df.columns if c!='target']+['target']]
        df=df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        return df

if __name__=='__main__':
    print(AirQualityDataset().get_data().head()) 
    # ------------------------------------------------------------------
    # Agent-aware feature engineering hooks (Air Quality)
    # ------------------------------------------------------------------
    def get_feature_agent(self, provider: str = "GPT5"):
        return {"provider": provider, "name": "AirQualityFeatureAgent", "version": "v1"}

    def _propose_agent_feature_plan(self, df: pd.DataFrame, agent) -> list:
        import numpy as np
        eps = 1e-6
        def has_all(cols):
            return all(c in df.columns for c in cols)
        plan = []

        # Time-based features
        if has_all(["Date", "Time"]):
            # Would need to parse date/time first
            pass
        
        # Pollutant interactions
        if has_all(["CO(GT)", "C6H6(GT)"]):
            plan.append({"name": "co_benzene_ratio", "requires": ["CO(GT)", "C6H6(GT)"],
                        "builder": lambda d: d["CO(GT)"] / (d["C6H6(GT)"] + eps)})
            plan.append({"name": "co_benzene_product", "requires": ["CO(GT)", "C6H6(GT)"],
                        "builder": lambda d: d["CO(GT)"] * d["C6H6(GT)"] / 100})
        
        # NOx features
        if has_all(["NOx(GT)", "NO2(GT)"]):
            plan.append({"name": "no_concentration", "requires": ["NOx(GT)", "NO2(GT)"],
                        "builder": lambda d: d["NOx(GT)"] - d["NO2(GT)"]})  # NO = NOx - NO2
            plan.append({"name": "no2_nox_ratio", "requires": ["NOx(GT)", "NO2(GT)"],
                        "builder": lambda d: d["NO2(GT)"] / (d["NOx(GT)"] + eps)})
        
        # Temperature and humidity effects
        if has_all(["T", "RH"]):
            plan.append({"name": "temp_humidity_index", "requires": ["T", "RH"],
                        "builder": lambda d: d["T"] * d["RH"] / 100})
            plan.append({"name": "apparent_temp", "requires": ["T", "RH"],
                        "builder": lambda d: d["T"] + 0.5555 * (6.112 * np.exp(17.67 * d["T"] / (d["T"] + 243.5)) * d["RH"] / 100 - 10)})
        
        # Temperature effects on sensors
        if has_all(["T", "PT08.S1(CO)"]):
            plan.append({"name": "co_sensor_temp_corrected", "requires": ["T", "PT08.S1(CO)"],
                        "builder": lambda d: d["PT08.S1(CO)"] * (1 + 0.01 * (d["T"] - 20))})
        
        # Sensor ratios (cross-sensitivity indicators)
        if has_all(["PT08.S1(CO)", "PT08.S2(NMHC)"]):
            plan.append({"name": "sensor_co_nmhc_ratio", "requires": ["PT08.S1(CO)", "PT08.S2(NMHC)"],
                        "builder": lambda d: d["PT08.S1(CO)"] / (d["PT08.S2(NMHC)"] + eps)})
        
        if has_all(["PT08.S3(NOx)", "PT08.S4(NO2)"]):
            plan.append({"name": "sensor_nox_no2_ratio", "requires": ["PT08.S3(NOx)", "PT08.S4(NO2)"],
                        "builder": lambda d: d["PT08.S3(NOx)"] / (d["PT08.S4(NO2)"] + eps)})
        
        # Absolute humidity from T and RH
        if has_all(["T", "RH"]):
            plan.append({"name": "absolute_humidity", "requires": ["T", "RH"],
                        "builder": lambda d: 6.112 * np.exp(17.67 * d["T"] / (d["T"] + 243.5)) * d["RH"] * 2.1674 / (273.15 + d["T"])})
        
        # Pollution index combining multiple pollutants
        if has_all(["CO(GT)", "NO2(GT)", "C6H6(GT)"]):
            plan.append({"name": "pollution_index", "requires": ["CO(GT)", "NO2(GT)", "C6H6(GT)"],
                        "builder": lambda d: (d["CO(GT)"] / 10 + d["NO2(GT)"] / 200 + d["C6H6(GT)"] / 5) / 3})
        
        # Sensor response patterns
        if has_all(["PT08.S1(CO)", "PT08.S2(NMHC)", "PT08.S3(NOx)", "PT08.S4(NO2)", "PT08.S5(O3)"]):
            plan.append({"name": "sensor_sum", "requires": ["PT08.S1(CO)", "PT08.S2(NMHC)", "PT08.S3(NOx)", "PT08.S4(NO2)", "PT08.S5(O3)"],
                        "builder": lambda d: d["PT08.S1(CO)"] + d["PT08.S2(NMHC)"] + d["PT08.S3(NOx)"] + d["PT08.S4(NO2)"] + d["PT08.S5(O3)"]})
        
        return plan

    @staticmethod
    def expand_features_on_dataframe(df: pd.DataFrame) -> (pd.DataFrame, list):
        self_like = AirQualityDataset()
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
        df, added = AirQualityDataset.expand_features_on_dataframe(df)
        try:
            df.attrs["agent_expansion_applied"] = True
            df.attrs["agent_provider"] = agent_provider
            df.attrs["agent_expanded_features"] = added
        except Exception:
            pass
        return df
