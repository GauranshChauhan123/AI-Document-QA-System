from pathlib import Path
from backend.bm25_store import build_bm25_index
from backend.config import PDF_DIR
from backend.pdf_loader import load_pdf
from backend.text_splitter import split_documents
from backend.vector_store import create_vector_store

class IngestionPipeline:

    def ingest(self, pdf_paths=None):
        documents = []

        if pdf_paths is not None:
            pdf_files = [Path(p) for p in pdf_paths]
        else:
            PDF_DIR.mkdir(parents=True, exist_ok=True)
            pdf_files = list(PDF_DIR.glob("*.pdf"))

        if not pdf_files:
            raise ValueError("No PDF files found to ingest.")

        for pdf in pdf_files:
            documents.extend(load_pdf(str(pdf)))

        if not documents:
            raise ValueError("No text content could be extracted from the PDF files.")

        chunks = split_documents(documents)

        if not chunks:
            raise ValueError("No text chunks generated from the documents.")

        vector_db = create_vector_store(chunks)

        build_bm25_index(chunks)

        # save_vector_store(vector_db)

        return {
            "documents": len(documents),
            "chunks": len(chunks)
        }

if __name__== "__main__":
    print(IngestionPipeline().ingest())