from backend.config import TOP_K, FETCH_K
from backend.vector_store import load_vector_store

class Retriever:

    def __init__(self):
        self.db = load_vector_store()

    def retrieve(self,query):

        return self.db.max_marginal_relevance_search(
            query=query,
            k=TOP_K,
            fetch_k=FETCH_K
        )
