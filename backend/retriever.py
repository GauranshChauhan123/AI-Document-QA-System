
import json

from backend.config import TOP_K, FETCH_K
from backend.vector_store import load_vector_store
from backend.bm25_store import load_bm25_index


RRF_K = 60


class Retriever:

    def __init__(self):
        self.db = load_vector_store()
        self.bm25, self.chunks = load_bm25_index()

    def _get_document_key(self, doc):
        return (
            doc.page_content,
            json.dumps(doc.metadata, sort_keys=True, default=str)
        )

    def retrieve(self, query):

        # Dense retrieval using ChromaDB
        dense_results = self.db.max_marginal_relevance_search(
            query=query,
            k=TOP_K,
            fetch_k=FETCH_K
        )

        # Sparse retrieval using BM25
        tokenized_query = query.lower().split()

        bm25_scores = self.bm25.get_scores(tokenized_query)

        sparse_indices = sorted(
            range(len(bm25_scores)),
            key=lambda i: bm25_scores[i],
            reverse=True
        )[:FETCH_K]

        sparse_results = [
            self.chunks[i] for i in sparse_indices
        ]

        # Reciprocal Rank Fusion
        rrf_scores = {}
        documents = {}

        for results in [dense_results, sparse_results]:

            for rank, doc in enumerate(results, start=1):

                key = self._get_document_key(doc)

                rrf_scores[key] = (
                    rrf_scores.get(key, 0)
                    + 1 / (RRF_K + rank)
                )

                documents[key] = doc

        # Sort documents by combined RRF score
        ranked_documents = sorted(
            rrf_scores,
            key=rrf_scores.get,
            reverse=True
        )

        return [
            documents[key]
            for key in ranked_documents[:TOP_K]
        ]


if __name__ == "__main__":

    retriever = Retriever()

    docs = retriever.retrieve(
        "What is supervised and unsupervised learning?"
    )

    for i, doc in enumerate(docs, 1):
        print(f"\n--- Document {i} ---")
        print(doc.page_content)
