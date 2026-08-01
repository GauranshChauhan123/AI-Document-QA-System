from pathlib import Path

from backend.config import PDF_DIR
from backend.pdf_loader import load_pdf
from backend.text_splitter import split_documents
from backend.vector_store import create_vector_store, save_vector_store


class IngestionPipeline:

    def ingest(self):
        documents = []

        pdf_files = list(PDF_DIR.glob("*.pdf"))

        if not pdf_files:
            raise ValueError("No PDF files found.")

        for pdf in pdf_files:
            documents.extend(load_pdf(str(pdf)))

        chunks = split_documents(documents)

        vector_db = create_vector_store(chunks)

        save_vector_store(vector_db)

        return {
            "documents": len(documents),
            "chunks": len(chunks)
        }