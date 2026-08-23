from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.ask import router as ask_router
from backend.routes.health import router as health_router
from backend.routes.upload import router as upload_router

app = FastAPI(
    title="Document RAG API",
    version="1.0.0"
)

# Allow the Streamlit frontend (and localhost dev) to reach this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten in production to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(upload_router)
app.include_router(ask_router)
