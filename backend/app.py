from fastapi import FastAPI

from backend.routes.ask import router as ask_router
from backend.routes.health import router as health_router
from backend.routes.upload import router as upload_router

app = FastAPI(
    title="Document RAG API",
    version="1.0.0"
)

app.include_router(health_router)
app.include_router(upload_router)
app.include_router(ask_router)
