import pandas as pd
import re
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parents[3]
RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "olist_order_reviews_dataset.csv"
PROCESSED_DATA_PATH = BASE_DIR / "data" / "processed" / "reviews_clean.csv"

def clean_text(text: str) -> str:
    """
    Cleans raw review text by removing HTML tags and excessive whitespace.
    """
    if not isinstance(text, str):
        return ""
    
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def process_dataset():
    if not RAW_DATA_PATH.exists():
        print(f"❌ Error: File not found at {RAW_DATA_PATH}")
        print("Please download the Olist dataset and place 'olist_order_reviews_dataset.csv' in data/raw/")
        return

    print(f"🔄 Loading data from {RAW_DATA_PATH}...")
    df = pd.read_csv(RAW_DATA_PATH)
    
    print(f"📊 Initial rows: {len(df)}")

    # 1. Rename columns to standard schema
    # Olist specific columns mapping
    df = df.rename(columns={
        'review_comment_message': 'review_text',
        'review_score': 'rating',
        'review_creation_date': 'date',
        'review_id': 'id'
    })

    # 2. Drop rows with empty reviews (Olist has many reviews with only ratings)
    df = df.dropna(subset=['review_text'])
    df['review_text'] = df['review_text'].apply(clean_text)
    
    # Filter out very short reviews (less than 10 chars) as they likely lack semantic meaning
    df = df[df['review_text'].str.len() > 10]

    # 3. Format Date
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

    # 4. Create Embedding Context
    # Combine rating + text to give the LLM better semantic understanding
    df['embedding_context'] = df.apply(
        lambda x: f"Rating: {x['rating']}/5. Review: {x['review_text']}", axis=1
    )

    print(f"✅ Cleaned data rows: {len(df)}")
    
    # Save processed data
    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"💾 Saved processed data to {PROCESSED_DATA_PATH}")

if __name__ == "__main__":
    process_dataset()