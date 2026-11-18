from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
PDF_PATH = PROJECT_DIR / "data" / "genai_notes.pdf"
SOURCE_PATH = "data/genai_notes.pdf"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

LLM_MODEL = "llama3.2"

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200

TOP_K = 3

COLLECTION_NAME = "genai_notes"

DB_PATH = str(PROJECT_DIR / "db")