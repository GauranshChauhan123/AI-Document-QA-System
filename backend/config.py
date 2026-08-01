from pathlib import Path
import os
from dotenv import load_dotenv

# ---------------- Paths ---------------- #

BASE_DIR = Path(__file__).resolve().parent.parent

# Load the project-local configuration regardless of the working directory used
# to start Uvicorn.
load_dotenv(BASE_DIR / "backend" / ".env")

DATA_DIR = BASE_DIR / "data"

PDF_DIR = DATA_DIR / "pdfs"

VECTOR_DB_DIR = BASE_DIR / "faiss_db"

# ---------------- Gemini ---------------- #

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = "gemini-2.5-flash"

# ---------------- Chunking ---------------- #

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200

# ---------------- Retrieval ---------------- #

TOP_K = 3

FETCH_K = 10

# ---------------- Embedding ---------------- #

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
