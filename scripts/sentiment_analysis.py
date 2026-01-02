import pandas as pd
from transformers import pipeline
import os

# load model ONCE
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment"
)

def classify_sentiment(text):
    if not isinstance(text, str) or text.strip() == "":
        return None, None

    result = sentiment_pipeline(text[:512])[0]  # model limit
    return result["label"], result["score"]

def sentiment_analysis(data_path):
    df = pd.read_csv(data_path)

    # schema check
    required_columns = {"text_en"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Invalid data structure. Missing columns: {missing}")

    df[["sentiment", "sentiment_confidence"]] = df["text_en"].apply(
        lambda x: pd.Series(classify_sentiment(x))
    )

    label_map = {
        "LABEL_0": "negative",
        "LABEL_1": "neutral",
        "LABEL_2": "positive"
    }
    df["sentiment"] = df["sentiment"].map(label_map)

    return df

def sentiment_analysis_df(df):
    # schema check
    required_columns = {"text_en"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Invalid data structure. Missing columns: {missing}")

    df[["sentiment", "sentiment_confidence"]] = df["text_en"].apply(
        lambda x: pd.Series(classify_sentiment(x))
    )

    label_map = {
        "LABEL_0": "negative",
        "LABEL_1": "neutral",
        "LABEL_2": "positive"
    }
    df["sentiment"] = df["sentiment"].map(label_map)

    return df

def run_sentiment_and_save(src_path, dest_path):
    df_sentiment = sentiment_analysis(src_path)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    df_sentiment.to_csv(dest_path, index=False)

    return df_sentiment
