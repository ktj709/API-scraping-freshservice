import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load .env file
load_dotenv()

@dataclass
class Config:
    # Scraping
    START_URL: str = "https://api.freshservice.com/#ticket_attributes"
    ALLOWED_DOMAINS = ("api.freshservice.com",)

    # Paths
    DATA_DIR: str = os.path.join(os.path.dirname(__file__), "data")
    RAW_JSON: str = os.path.join(DATA_DIR, "raw_freshservice_docs.json")
    PROCESSED_JSON: str = os.path.join(DATA_DIR, "processed_chunks.json")
    INDEX_PATH: str = os.path.join(DATA_DIR, "vector_index.pkl")
    METADATA_PATH: str = os.path.join(DATA_DIR, "vector_metadata.pkl")

    # Chunking
    CHUNK_SIZE: int = 800       # 🔹 slightly smaller for better granularity
    CHUNK_OVERLAP: int = 150

    # Embeddings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # LLM (Gemini)
    USE_GEMINI_LLM: bool = True
    GEMINI_MODEL: str = "gemini-1.5-flash"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")

    # Retrieval
    TOP_K: int = 8   # 🔹 increased to send more context to Gemini

def ensure_dirs():
    os.makedirs(Config.DATA_DIR, exist_ok=True)
