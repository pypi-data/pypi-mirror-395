import os
import pandas as pd
import requests
from app.datasets.BaseDatasetLoader import BaseDatasetLoader

class TwitterSentimentDataset(BaseDatasetLoader):
    """Twitter Sentiment Analysis Dataset.

    Real dataset for sentiment classification based on Twitter messages.
    Dataset contains tweets with sentiment labels (positive/negative).
    Used for social media analysis and opinion mining research.
    Target: Sentiment (1=positive, 0=negative).
    
    Source: https://raw.githubusercontent.com/dD2405/Twitter_Sentiment_Analysis/master/train.csv
    Original: Twitter API data with sentiment annotations
    """

    def get_dataset_info(self):
        return {
            "name": "TwitterSentimentDataset",
            "source_id": "social_science:twitter_sentiment",
            "source_url": "https://raw.githubusercontent.com/dD2405/Twitter_Sentiment_Analysis/master/train.csv",
            "category": "binary_classification",
            "description": "Twitter sentiment analysis from tweet features. Target: sentiment (1=positive, 0=negative).",
            "target_column": "label",
        }

    def download_dataset(self, info):
        """Override to implement fallback URLs"""
        dataset_name = info["name"]
        urls = [
            "https://raw.githubusercontent.com/dD2405/Twitter_Sentiment_Analysis/master/train.csv",
            "https://raw.githubusercontent.com/shayneobrien/algorithmic-trading-bot/master/sentiment/train.csv"
        ]
        
        for i, url in enumerate(urls):
            try:
                print(f"[{dataset_name}] Trying URL {i+1}: {url}")
                r = requests.get(url, timeout=30)
                print(f"[{dataset_name}] HTTP {r.status_code}")
                if r.status_code == 200:
                    print(f"[{dataset_name}] Successfully downloaded from URL {i+1}")
                    return r.content
            except Exception as e:
                print(f"[{dataset_name}] URL {i+1} failed: {e}")
                continue
        
        raise RuntimeError(f"[{dataset_name}] All download URLs failed")

    def process_dataframe(self, df, info):
        dataset_name = info["name"]
        target_col_original = info["target_column"]
        print(f"[{dataset_name}] Raw shape: {df.shape}")

        # Check for different possible target column names
        possible_targets = ["label", "target", "sentiment", "class"]
        actual_target = None
        
        for target in possible_targets:
            if target in df.columns:
                actual_target = target
                break
        
        if actual_target is None:
            # If no standard target found, assume last column is target
            actual_target = df.columns[-1]
            print(f"[{dataset_name}] No standard target column found, using last column: {actual_target}")

        # Target conversion based on data type
        if df[actual_target].dtype == 'object':
            # Map positive sentiment to 1, negative to 0
            sentiment_map = {"positive": 1, "negative": 0, "1": 1, "0": 0, "pos": 1, "neg": 0}
            df["target"] = df[actual_target].map(sentiment_map)
            # Handle any unmapped values
            if df["target"].isna().any():
                df["target"] = df["target"].fillna(0)
        else:
            # If numeric, assume already 0/1
            df["target"] = pd.to_numeric(df[actual_target], errors="coerce").astype(int)
        
        if actual_target != "target":
            df.drop(columns=[actual_target], inplace=True)
        
        # Process text columns to create numeric features
        text_cols = ["tweet", "text", "message", "content"]
        for col in text_cols:
            if col in df.columns:
                # Create simple numeric features from text
                df["text_length"] = df[col].astype(str).apply(len)
                df["word_count"] = df[col].astype(str).apply(lambda x: len(x.split()))
                df["exclamation_count"] = df[col].astype(str).apply(lambda x: x.count('!'))
                df["question_count"] = df[col].astype(str).apply(lambda x: x.count('?'))
                df["mention_count"] = df[col].astype(str).apply(lambda x: x.count('@'))
                df["hashtag_count"] = df[col].astype(str).apply(lambda x: x.count('#'))
                df["capital_ratio"] = df[col].astype(str).apply(lambda x: sum(1 for c in x if c.isupper()) / (len(x) + 1))
                # Drop the original text column
                df.drop(columns=[col], inplace=True)

        # Drop id columns
        id_cols = ["id", "tweet_id", "user_id"]
        for col in id_cols:
            if col in df.columns:
                df.drop(columns=[col], inplace=True)

        # Convert all feature columns to numeric, coercing errors
        for col in df.columns:
            if col != "target":
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Drop rows with NA values
        before_dropna = len(df)
        df.dropna(inplace=True)
        if before_dropna > len(df):
            print(f"[{dataset_name}] Dropped {before_dropna - len(df)} rows with NA values.")

        # Deduplicate
        before_dedup = len(df)
        df.drop_duplicates(inplace=True)
        if len(df) < before_dedup:
            print(f"[{dataset_name}] Removed {before_dedup - len(df)} duplicate rows.")

        # Reorder columns so target last
        df = df[[c for c in df.columns if c != "target"] + ["target"]]

        # Shuffle
        df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)

        print(f"[{dataset_name}] Final shape: {df.shape}")
        print(f"[{dataset_name}] Target distribution: {df['target'].value_counts().to_dict()}")
        return df

if __name__ == "__main__":
    ds = TwitterSentimentDataset()
    frame = ds.get_data()
    print(frame.head())
    print(f"Target column: {frame.columns[-1]}")
    print(frame['target'].value_counts()) 