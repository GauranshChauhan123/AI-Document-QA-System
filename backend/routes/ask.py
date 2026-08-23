"""Question-answering endpoint."""

from fastapi import APIRouter, HTTPException

from backend.models import AskRequest, AskResponse

router = APIRouter(tags=["ask"])


@router.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    """Return an answer and the PDF passages used to produce it."""
    if not request.question.strip():
        raise HTTPException(status_code=422, detail="Question cannot be empty.")

    try:
        from backend.rag import RAGPipeline

        result = RAGPipeline().ask(request.question)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=400,
            detail="No documents have been indexed yet. Please upload a PDF first.",
        ) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Question answering failed: {exc}") from exc

    return AskResponse(**result)
