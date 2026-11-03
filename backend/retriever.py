from backend.config import TOP_K, FETCH_K,VECTOR_DB_DIR,PDF_DIR
import os
from backend.ingest import IngestionPipeline
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


if __name__ == "__main__":

    if not os.path.exists(VECTOR_DB_DIR):
        IngestionPipeline().ingest()
        
    retriever=Retriever()    
    docs = retriever.retrieve("What is supervised and unsupervised learning")
    for i, doc in enumerate(docs, 1):
       print(f"\n--- Document {i} ---")
       print(doc.page_content)
