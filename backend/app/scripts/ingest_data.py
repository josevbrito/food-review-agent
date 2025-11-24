import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Load environment variables
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

# Paths
BASE_DIR = Path(__file__).resolve().parents[3]
PROCESSED_DATA_PATH = BASE_DIR / "data" / "processed" / "reviews_clean.csv"
CHROMA_DB_DIR = BASE_DIR / "backend" / "chroma_db"

def ingest_data():
    if not PROCESSED_DATA_PATH.exists():
        print(f"❌ Error: Processed data not found at {PROCESSED_DATA_PATH}")
        return

    print("🔄 Loading processed data...")
    df = pd.read_csv(PROCESSED_DATA_PATH)
    
    df = df.head(1000) 
    print(f"📊 Ingesting {len(df)} reviews...")

    documents = []
    for _, row in df.iterrows():
        metadata = {
            "rating": row["rating"],
            "date": row["date"],
            "review_id": row["id"]
        }
        
        doc = Document(
            page_content=row["embedding_context"],
            metadata=metadata
        )
        documents.append(doc)

    # 2. Initialize Embeddings Model (OPEN SOURCE & FREE)
    # "all-MiniLM-L6-v2"
    print("📥 Loading HuggingFace Embedding Model (Runs locally)...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # 3. Create/Update Vector Store
    print("🧠 Generating embeddings and storing in ChromaDB...")
    
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name="restaurant_reviews",
        persist_directory=str(CHROMA_DB_DIR)
    )

    print(f"✅ Ingestion complete! Vector store saved at {CHROMA_DB_DIR}")

if __name__ == "__main__":
    ingest_data()