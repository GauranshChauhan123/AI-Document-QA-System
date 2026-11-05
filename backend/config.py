from pathlib import Path
import os
from dotenv import load_dotenv

# ---------------- Paths ---------------- #

# __file__ is  /app/backend/config.py  inside Docker → parent.parent = /app
# For local dev it resolves to the repo root — same behaviour.
BASE_DIR = Path(os.environ.get("APP_BASE_DIR", str(Path(__file__).resolve().parent.parent)))

# Load .env files (no-op if the files are absent; env vars already injected by Docker)
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR / "backend" / ".env")

DATA_DIR = BASE_DIR / "data"

PDF_DIR = DATA_DIR / "pdfs"

VECTOR_DB_DIR = BASE_DIR / "chroma_db"

# ---------------- Gemini ---------------- #

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

MODEL_NAME = "gemini-2.5-flash"

# ---------------- Chunking ---------------- #

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200

# ---------------- Retrieval ---------------- #

TOP_K = 6   

FETCH_K = 10

# ---------------- Embedding ---------------- #

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
