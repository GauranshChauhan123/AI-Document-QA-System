"""PDF upload and indexing endpoint."""

from pathlib import Path
from shutil import copyfileobj
from typing import List, Union
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from backend.config import PDF_DIR
from backend.models import UploadResponse

router = APIRouter(tags=["upload"])


@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
def upload_documents(
    files: Union[List[UploadFile], UploadFile] = File(...),
):
    """Save one or more PDFs and rebuild the vector index from all uploaded PDFs."""
    file_list = files if isinstance(files, list) else [files]

    if not file_list:
        raise HTTPException(status_code=400, detail="No files provided.")

    for f in file_list:
        if not f.filename or Path(f.filename).suffix.lower() != ".pdf":
            raise HTTPException(
                status_code=400,
                detail=f"Only PDF files are supported. Received: '{f.filename}'",
            )

    PDF_DIR.mkdir(parents=True, exist_ok=True)
    saved_filenames = []

    try:
        from backend.ingest import IngestionPipeline

        for f in file_list:
            safe_filename = Path(f.filename).name
            destination = PDF_DIR / safe_filename
            staging_path = PDF_DIR / f".{safe_filename}.{uuid4().hex}.upload"

            try:
                with staging_path.open("wb") as output:
                    copyfileobj(f.file, output)
                if destination.exists():
                    destination.unlink()
                staging_path.replace(destination)
                saved_filenames.append(safe_filename)
            finally:
                f.file.close()
                if staging_path.exists():
                    try:
                        staging_path.unlink()
                    except OSError:
                        pass

        result = IngestionPipeline().ingest()
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Document ingestion failed: {exc}"
        ) from exc

    file_summary = (
        saved_filenames[0]
        if len(saved_filenames) == 1
        else f"{len(saved_filenames)} files ({', '.join(saved_filenames)})"
    )

    return UploadResponse(
        message=f"Uploaded and indexed {file_summary}.",
        documents=result["documents"],
        chunks=result["chunks"],
    )
