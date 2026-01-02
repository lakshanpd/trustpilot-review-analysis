from dotenv import load_dotenv
import os 
from scripts.preprocessing import preprocess_pipeline_df
from scripts.scrape_trustpilot import scrape_reviews_to_dataframe
from scripts.sentiment_analysis import sentiment_analysis_df

load_dotenv()

TRUSTPILOT_URL = os.getenv("TRUSTPILOT_URL")
DEST_FILE = os.getenv("DEST_FILE")

def save_result(df, dest_path):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    df.to_csv(dest_path, index=False)

if __name__ == "__main__":
    df = scrape_reviews_to_dataframe(TRUSTPILOT_URL)
    print("\nweb scraping is completed\n")

    df = preprocess_pipeline_df(df)
    print("data preprocessing is completed\n")

    df = sentiment_analysis_df(df)
    save_result(df, DEST_FILE)
    print("sentiment analysis is completed\n")
    

