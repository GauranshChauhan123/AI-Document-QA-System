
import pickle
from pathlib import Path
from rank_bm25 import BM25Okapi

from backend.config import VECTOR_DB_DIR


BM25_INDEX_PATH = VECTOR_DB_DIR / "bm25_index.pkl"


def build_bm25_index(chunks):
    tokenized_chunks = [
        doc.page_content.lower().split()
        for doc in chunks
    ]

    bm25 = BM25Okapi(tokenized_chunks)

    VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)

    with open(BM25_INDEX_PATH, "wb") as f:
        pickle.dump(
            {
                "bm25": bm25,
                "chunks": chunks
            },
            f
        )

    return bm25


def load_bm25_index():
    if not BM25_INDEX_PATH.exists():
        raise FileNotFoundError("BM25 index not found. Ingest the PDF first.")

    with open(BM25_INDEX_PATH, "rb") as f:
        data = pickle.load(f)

    return data["bm25"], data["chunks"]
