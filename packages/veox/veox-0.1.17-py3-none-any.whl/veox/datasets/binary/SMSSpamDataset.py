import os
import pandas as pd
import requests
from io import BytesIO, TextIOWrapper
from zipfile import ZipFile
from app.datasets.BaseDatasetLoader import BaseDatasetLoader


class SMSSpamDataset(BaseDatasetLoader):
    """SMS Spam Collection Dataset (binary classification).

    5,574 SMS messages labelled as ham (0) or spam (1).
    Source: https://archive.ics.uci.edu/ml/datasets/sms+spam+collection
    """

    def get_dataset_info(self):
        return {
            "name": "SMSSpamDataset",
            "source_id": "uci:sms_spam_collection",
            "category": "binary_classification",
            "description": "SMS spam dataset – classify messages as ham or spam.",
        }

    def download_dataset(self, info):
        dataset_name = info["name"]
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip"
        print(f"[{dataset_name}] Downloading ZIP from {url}")
        try:
            r = requests.get(url, timeout=30)
            if r.status_code != 200:
                raise RuntimeError(f"HTTP {r.status_code}")
            return r.content
        except Exception as e:
            print(f"[{dataset_name}] Download error: {e}")
            raise

    def process_dataframe(self, df, info):
        # This method won't be used because we'll override get_data to handle zip extraction
        return df

    # Override get_data to handle zip extraction easily
    def get_data(self):
        info = self.get_dataset_info()
        dataset_name = info["name"]

        src_bytes = self.download_dataset(info)
        with ZipFile(BytesIO(src_bytes)) as zf:
            with zf.open("SMSSpamCollection") as f:
                text = TextIOWrapper(f, encoding="utf-8").read()
        lines = [line for line in text.splitlines() if line.strip()]
        labels = []
        messages = []
        for line in lines:
            label, msg = line.split("\t", 1)
            labels.append(1 if label == "spam" else 0)
            messages.append(msg)
        
        df = pd.DataFrame({"message": messages, "target": labels})
        
        # Extract features from text messages
        print(f"[{dataset_name}] Extracting features from text messages...")
        
        # Text statistics
        df['msg_length'] = df['message'].str.len()
        df['word_count'] = df['message'].str.split().str.len()
        df['avg_word_length'] = df['message'].apply(
            lambda x: sum(len(word) for word in x.split()) / (len(x.split()) + 1)
        )
        df['exclamation_count'] = df['message'].str.count('!')
        df['question_count'] = df['message'].str.count('\?')
        df['uppercase_ratio'] = df['message'].apply(
            lambda x: sum(1 for c in x if c.isupper()) / (len(x) + 1)
        )
        df['digit_ratio'] = df['message'].apply(
            lambda x: sum(1 for c in x if c.isdigit()) / (len(x) + 1)
        )
        df['special_char_count'] = df['message'].str.count('[^a-zA-Z0-9\s]')
        
        # Spam indicators
        df['has_free'] = df['message'].str.lower().str.contains('free').astype(int)
        df['has_win'] = df['message'].str.lower().str.contains('win').astype(int)
        df['has_prize'] = df['message'].str.lower().str.contains('prize').astype(int)
        df['has_claim'] = df['message'].str.lower().str.contains('claim').astype(int)
        df['has_call'] = df['message'].str.lower().str.contains('call').astype(int)
        df['has_text'] = df['message'].str.lower().str.contains('text').astype(int)
        df['has_mobile'] = df['message'].str.lower().str.contains('mobile').astype(int)
        df['has_cash'] = df['message'].str.lower().str.contains('cash').astype(int)
        df['has_urgent'] = df['message'].str.lower().str.contains('urgent').astype(int)
        df['has_offer'] = df['message'].str.lower().str.contains('offer').astype(int)
        
        # Currency symbols
        df['has_pound'] = df['message'].str.contains('£').astype(int)
        df['has_dollar'] = df['message'].str.contains('\$').astype(int)
        
        # Drop the original message column
        df = df.drop('message', axis=1)
        
        # Move target to end
        cols = [c for c in df.columns if c != 'target'] + ['target']
        df = df[cols]
        
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        print(f"[{dataset_name}] Loaded {len(df)} rows with {len(df.columns)} features.")
        print(f"[{dataset_name}] Target distribution: {df['target'].value_counts().to_dict()}")
        return df


if __name__ == "__main__":
    d = SMSSpamDataset()
    df = d.get_data()
    print(df.head()) 