from langchain_community.vectorstores import FAISS

from backend.config import VECTOR_DB_DIR
from backend.embeddings import get_embedding_model


def create_vector_store(chunks):
    embeddings = get_embedding_model()

    vector_db = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    return vector_db


def save_vector_store(vector_db):
    VECTOR_DB_DIR.parent.mkdir(parents=True, exist_ok=True)
    vector_db.save_local(str(VECTOR_DB_DIR))


def load_vector_store():
    if not VECTOR_DB_DIR.exists():
        raise FileNotFoundError("No vector index found. Upload a PDF before asking questions.")

    embeddings = get_embedding_model()

    db = FAISS.load_local(
        str(VECTOR_DB_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )

    return db
