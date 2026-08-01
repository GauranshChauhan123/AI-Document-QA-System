from functools import lru_cache

from langchain_community.embeddings import HuggingFaceEmbeddings

from backend.config import EMBEDDING_MODEL


@lru_cache(maxsize=1)
def get_embedding_model():
    """Initialize the embedding model only when it is first needed."""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
