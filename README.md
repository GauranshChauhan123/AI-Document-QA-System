# 📄 AI Document QA System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.60-FF4B4B?logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=github-actions&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

**An AI-powered Retrieval-Augmented Generation (RAG) system that lets you upload PDF documents and ask questions about them — answered by Google Gemini 2.5 Flash.**

[Features](#-features) · [Architecture](#-architecture) · [Quick Start](#-quick-start-docker) · [Local Dev](#️-local-development) · [API Docs](#-api-reference) · [CI/CD](#-cicd-pipeline)

</div>

---

## 🚀 Features

- 📤 **Multi-PDF Upload** — upload one or more PDFs in a single request
- 🔍 **Semantic Search** — FAISS vector store with `all-MiniLM-L6-v2` embeddings
- 🤖 **Gemini 2.5 Flash** — fast, accurate answers grounded in your documents
- 📌 **Source Citations** — every answer includes the source file and page number
- 💬 **Chat Interface** — clean Streamlit UI with full conversation history
- 🐳 **Docker Ready** — one command to spin up the entire stack
- 🔄 **CI/CD Pipeline** — GitHub Actions: lint → test → build → integration test → push to Docker Hub
- 🌐 **REST API** — FastAPI backend with auto-generated Swagger docs

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **LLM** | Google Gemini 2.5 Flash (`gemini-2.5-flash`) |
| **Embeddings** | Sentence Transformers `all-MiniLM-L6-v2` |
| **Vector Store** | FAISS (CPU) |
| **RAG Framework** | LangChain |
| **PDF Parsing** | PyMuPDF |
| **Backend API** | FastAPI + Uvicorn |
| **Frontend UI** | Streamlit |
| **Containerization** | Docker + Docker Compose |
| **CI/CD** | GitHub Actions → Docker Hub |

---

## 📂 Project Structure

```text
pdf_QA/
├── backend/                    # FastAPI application
│   ├── app.py                  # App factory + CORS middleware
│   ├── config.py               # Paths, env vars, model config
│   ├── embeddings.py           # Sentence Transformer loader
│   ├── ingest.py               # Ingestion pipeline orchestrator
│   ├── llm.py                  # Gemini client wrapper
│   ├── models.py               # Pydantic request/response models
│   ├── pdf_loader.py           # PyMuPDF PDF loader
│   ├── prompts.py              # RAG prompt templates
│   ├── rag.py                  # RAG pipeline (retrieve → augment → generate)
│   ├── retriever.py            # FAISS retriever wrapper
│   ├── text_splitter.py        # Recursive character text splitter
│   ├── vector_store.py         # FAISS create / save / load helpers
│   ├── routes/
│   │   ├── ask.py              # POST /ask
│   │   ├── health.py           # GET  /health
│   │   └── upload.py           # POST /upload
│   └── Dockerfile
│
├── frontend/                   # Streamlit application
│   ├── app.py                  # Main Streamlit entry point
│   ├── api.py                  # HTTP client (upload / ask / health)
│   ├── config.py               # BACKEND_URL (env-aware)
│   ├── styles.py               # Custom CSS loader
│   ├── components/
│   │   ├── chat.py             # Chat history + input handling
│   │   ├── sidebar.py          # PDF upload sidebar
│   │   └── source_card.py      # Source citation card
│   └── Dockerfile
│
├── data/pdfs/                  # Uploaded PDFs (Docker volume)
├── faiss_db/                   # FAISS index (Docker volume)
├── .github/workflows/ci.yml    # CI/CD pipeline
├── .env                        # API keys (never commit this)
├── .dockerignore
├── docker-compose.yml
├── requirements-backend.txt
├── requirements-frontend.txt
└── requirements.txt            # Full pinned deps (local dev)
```

---

## 🐳 Quick Start (Docker)

> **Prerequisites:** Docker Desktop installed and running.

### 1. Clone the repo

```bash
git clone https://github.com/GauranshChauhan123/AI-Document-QA-System.git
cd AI-Document-QA-System
```

### 2. Add your Gemini API key

```bash
# Create .env in the project root
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
```

> Get a free key at [aistudio.google.com](https://aistudio.google.com/app/apikey)

### 3. Start the stack

```bash
docker compose up --build
```

| Service | URL |
|---|---|
| 🖥 Streamlit UI | http://localhost:8501 |
| ⚡ FastAPI Backend | http://localhost:8000 |
| 📖 Swagger Docs | http://localhost:8000/docs |

> The frontend waits for the backend to pass its health check before starting.

### 4. Stop the stack

```bash
docker compose down          # stop containers (data volumes preserved)
docker compose down -v       # stop + delete all data volumes
```

---

## 🖥️ Local Development

### 1. Clone & create virtual environment

```bash
git clone https://github.com/GauranshChauhan123/AI-Document-QA-System.git
cd AI-Document-QA-System

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements-backend.txt
pip install -r requirements-frontend.txt
```

### 3. Create `.env`

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Run the backend

```bash
uvicorn backend.app:app --reload
```

### 5. Run the frontend (new terminal)

```bash
streamlit run frontend/app.py
```

---

## 💬 How It Works

```
1. Upload PDF(s)
       │
       ▼
2. PyMuPDF extracts text
       │
       ▼
3. Text split into overlapping chunks (1000 chars / 200 overlap)
       │
       ▼
4. Chunks embedded → all-MiniLM-L6-v2 (384-dim vectors)
       │
       ▼
5. Vectors stored in FAISS index (saved to disk)
       │
       ▼
6. User asks a question
       │
       ▼
7. Question embedded → top-K chunks retrieved via MMR search
       │
       ▼
8. Context + question sent to Gemini 2.5 Flash
       │
       ▼
9. Answer + source citations returned to the UI
```

---

## 🧠 Architecture

```
┌─────────────────────────────────────────┐
│            Streamlit Frontend           │
│         http://localhost:8501           │
└──────────────────┬──────────────────────┘
                   │  HTTP (REST)
┌──────────────────▼──────────────────────┐
│             FastAPI Backend             │
│         http://localhost:8000           │
│                                         │
│  POST /upload ──► Ingest Pipeline       │
│                   ├─ PyMuPDF loader     │
│                   ├─ Text splitter      │
│                   ├─ MiniLM embeddings  │
│                   └─ FAISS index        │
│                                         │
│  POST /ask ─────► RAG Pipeline          │
│                   ├─ FAISS retrieval    │
│                   ├─ Context assembly   │
│                   └─ Gemini 2.5 Flash   │
│                                         │
│  GET  /health ──► {"status":"healthy"}  │
└─────────────────────────────────────────┘
```

---

## 📡 API Reference

### `GET /health`
Returns server status.
```json
{ "status": "healthy" }
```

### `POST /upload`
Upload one or more PDF files for indexing.

| Field | Type | Description |
|---|---|---|
| `files` | `File[]` | One or more `.pdf` files |

**Response `201`:**
```json
{
  "message": "Uploaded and indexed report.pdf.",
  "documents": 1,
  "chunks": 42
}
```

### `POST /ask`
Ask a question against the indexed documents.

**Request body:**
```json
{ "question": "What are the key findings?" }
```

**Response `200`:**
```json
{
  "answer": "The key findings are ...",
  "sources": [
    { "file": "report.pdf", "page": 3, "content": "..." }
  ]
}
```

---

## 🔄 CI/CD Pipeline

The pipeline runs automatically on every push to `main` or `develop`.

```
push / PR
    │
    ├─► lint          flake8 + black (backend & frontend)
    │
    ├─► test-backend  pytest backend/test*.py
    │
    ├─► build         docker buildx (backend + frontend images)
    │                 ↳ artifacts uploaded for next job
    │
    ├─► integration-test
    │       docker compose up → health-check → smoke test
    │
    └─► push-images   (main branch only)
            docker push gauranshchauhan123/pdf-qa-backend
            docker push gauranshchauhan123/pdf-qa-frontend
```

### Docker Hub Images

| Image | Pull |
|---|---|
| Backend | `docker pull gauranshchauhan123/pdf-qa-backend` |
| Frontend | `docker pull gauranshchauhan123/pdf-qa-frontend` |

### Required GitHub Secrets

| Secret | Value |
|---|---|
| `DOCKERHUB_USERNAME` | `gauranshchauhan123` |
| `DOCKERHUB_TOKEN` | Docker Hub Access Token |

---

## ⚙️ Configuration

All tuneable parameters live in [`backend/config.py`](backend/config.py):

| Variable | Default | Description |
|---|---|---|
| `MODEL_NAME` | `gemini-2.5-flash` | Gemini model |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence Transformer |
| `CHUNK_SIZE` | `1000` | Characters per chunk |
| `CHUNK_OVERLAP` | `200` | Overlap between chunks |
| `TOP_K` | `3` | Chunks returned per query |
| `FETCH_K` | `10` | Candidates before MMR re-ranking |

---

## 🔮 Roadmap

- [ ] Streaming responses (Server-Sent Events)
- [ ] Conversation memory / multi-turn chat
- [ ] Persistent document management (re-upload without re-indexing)
- [ ] User authentication
- [ ] Citation highlighting in source text
- [ ] Cloud deployment (GCP Cloud Run / AWS ECS)
- [ ] Support for DOCX, TXT, and web URLs

---

## 👨‍💻 Author

**Gauransh Chauhan**

[![GitHub](https://img.shields.io/badge/GitHub-GauranshChauhan123-181717?logo=github)](https://github.com/GauranshChauhan123)
[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-gauranshchauhan123-2496ED?logo=docker)](https://hub.docker.com/u/gauranshchauhan123)

---

## ⭐ Star this repo if you found it useful!