"""PDF upload and indexing endpoint."""

from pathlib import Path
from shutil import copyfileobj
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from backend.config import PDF_DIR
from backend.models import UploadResponse

router = APIRouter(tags=["upload"])


@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
def upload_document(file: UploadFile = File(...)):
    """Save a PDF and rebuild the vector index from all uploaded PDFs."""
    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    PDF_DIR.mkdir(parents=True, exist_ok=True)
    destination = PDF_DIR / Path(file.filename).name
    staging_path = PDF_DIR / f".{destination.name}.{uuid4().hex}.upload"
    backup_path = PDF_DIR / f".{destination.name}.{uuid4().hex}.backup"
    had_existing_file = destination.exists()
    original_moved = False
    replacement_installed = False

    try:
        # Delay model initialization until a document needs indexing.
        from backend.ingest import IngestionPipeline

        with staging_path.open("wb") as output:
            copyfileobj(file.file, output)

        if had_existing_file:
            destination.replace(backup_path)
            original_moved = True
        staging_path.replace(destination)
        replacement_installed = True

        result = IngestionPipeline().ingest()
    except Exception as exc:
        if replacement_installed and destination.exists():
            destination.unlink()
        if original_moved and backup_path.exists():
            backup_path.replace(destination)
        raise HTTPException(status_code=500, detail=f"Document ingestion failed: {exc}") from exc
    finally:
        file.file.close()
        if staging_path.exists():
            staging_path.unlink()
        if backup_path.exists():
            backup_path.unlink()

    return UploadResponse(
        message=f"Uploaded and indexed {destination.name}.",
        documents=result["documents"],
        chunks=result["chunks"],
    )
