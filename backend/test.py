from pathlib import Path

from backend.ingest import IngestionPipeline

BASE_DIR = Path(__file__).resolve().parent.parent

pdf_folder = BASE_DIR / "data" / "pdfs"

pdfs = list(pdf_folder.glob("*.pdf"))

pipeline = IngestionPipeline()

docs, chunks = pipeline.ingest(pdfs)

print(f"Loaded {docs} pages")
print(f"Created {chunks} chunks")
