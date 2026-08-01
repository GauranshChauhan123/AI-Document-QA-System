from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str


class Source(BaseModel):
    file: str
    page: int
    content: str


class AskResponse(BaseModel):
    answer: str
    sources: list[Source]


class UploadResponse(BaseModel):
    message: str
    documents: int
    chunks: int