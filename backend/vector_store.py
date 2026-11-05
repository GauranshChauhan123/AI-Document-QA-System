
from langchain_chroma import Chroma
from backend.config import VECTOR_DB_DIR
from backend.embeddings import get_embedding_model


def create_vector_store(chunks):
    embeddings = get_embedding_model()

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(VECTOR_DB_DIR)
    )

    return vector_db


# def save_vector_store(vector_db):
#     VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)
#     vector_db.save_local(str(VECTOR_DB_DIR))


def load_vector_store():
    if not VECTOR_DB_DIR.exists() or not (VECTOR_DB_DIR / "chroma.sqlite3").exists():
        raise FileNotFoundError("No vector index found. Upload a PDF before asking questions.")

    embeddings = get_embedding_model()

    db = Chroma(
        persist_directory=str(VECTOR_DB_DIR),
        embedding_function=embeddings
    )

    return db
