import pandas as pd
from deep_translator import GoogleTranslator
from langdetect import detect, LangDetectException
import os

def detect_language_safe(text):
    if not isinstance(text, str) or len(text.split()) < 5:
        return None
    try:
        return detect(text)
    except LangDetectException:
        return None

def translate_to_english(text, lang):
    translator = GoogleTranslator(source="auto", target="en")
    
    if not text or lang in (None, "en"):
        return text
    try:
        return translator.translate(text)
    except Exception:
        return None

def preprocess_pipeline(data_path, review_count_threshold=5):
    df = pd.read_csv(data_path)

    # schema check
    required_columns = {"reviewer", "date", "text", "stars"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Invalid data structure. Missing columns: {missing}")
        
    # drop rows with null values
    df.dropna(inplace=True)

    # drop records of reviewers who has more than review_count_threshold reviews
    review_counts = df.groupby("reviewer").size()
    valid_reviewers = review_counts[review_counts <= review_count_threshold].index
    df = df[df["reviewer"].isin(valid_reviewers)].copy()

    # convert date column to datetime
    df["datetime"] = pd.to_datetime(df["date"], utc=True)
    df.drop(columns=['date'], inplace=True)

    # create language column
    df["language"] = df["text"].apply(detect_language_safe)

    # translate to english
    df["text_en"] = df.apply(
        lambda row: translate_to_english(row["text"], row["language"]),
        axis=1
    )

    return df.reset_index(drop=True)

def preprocess_pipeline_df(df, review_count_threshold=5):
    # schema check
    required_columns = {"reviewer", "date", "text", "stars"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Invalid data structure. Missing columns: {missing}")
        
    # drop rows with null values
    df.dropna(inplace=True)

    # drop records of reviewers who has more than review_count_threshold reviews
    review_counts = df.groupby("reviewer").size()
    valid_reviewers = review_counts[review_counts <= review_count_threshold].index
    df = df[df["reviewer"].isin(valid_reviewers)].copy()

    # convert date column to datetime
    df["datetime"] = pd.to_datetime(df["date"], utc=True)
    df.drop(columns=['date'], inplace=True)

    # create language column
    df["language"] = df["text"].apply(detect_language_safe)

    # translate to english
    df["text_en"] = df.apply(
        lambda row: translate_to_english(row["text"], row["language"]),
        axis=1
    )

    return df.reset_index(drop=True)

def run_preprocessing_and_save(src_path, dest_path, review_count_threshold=5):
    """
    Runs the preprocessing pipeline on src_path and saves the cleaned CSV to dest_path.
    """
    # run pipeline
    df_clean = preprocess_pipeline(
        data_path=src_path,
        review_count_threshold=review_count_threshold
    )

    # ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # save output
    df_clean.to_csv(dest_path, index=False)

    return df_clean
