# 📄 AI Document Question Answering System

An AI-powered Document Question Answering System built using **FastAPI**, **LangChain**, **FAISS**, **Google Gemini**, and **Streamlit**.

The application allows users to upload one or more PDF documents, builds a semantic vector index, and answers questions using Retrieval-Augmented Generation (RAG).

---

## 🚀 Features

- Upload multiple PDF documents
- Automatic document indexing
- Semantic search using FAISS
- Google Gemini for answer generation
- ChatGPT-style Streamlit interface
- Source citation with page numbers
- FastAPI backend
- Modular architecture
- Docker-ready (coming soon)

---

## 🛠 Tech Stack

### Backend

- FastAPI
- LangChain
- FAISS
- PyMuPDF
- Sentence Transformers
- Google Gemini

### Frontend

- Streamlit

### AI

- Gemini 2.5 Flash
- all-MiniLM-L6-v2 Embeddings

---

## 📂 Project Structure

```text
RAG_QA/
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── embeddings.py
│   ├── ingest.py
│   ├── llm.py
│   ├── models.py
│   ├── pdf_loader.py
│   ├── rag.py
│   ├── retriever.py
│   ├── routes/
│   ├── text_splitter.py
│   └── vector_store.py
│
├── frontend/
│   ├── app.py
│   ├── api.py
│   ├── config.py
│   ├── styles.py
│   └── components/
│
├── data/
│
├── faiss_db/
│
├── requirements.txt
│
└── README.md
```

---

## ⚙ Installation

### Clone Repository

```bash
git clone https://github.com/GauranshChauhan123/RAG_QA.git

cd RAG_QA
```

---

### Create Virtual Environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Create Environment Variables

Create a `.env` file.

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

---

## ▶ Run Backend

```bash
uvicorn backend.app:app --reload
```

Backend

```
http://127.0.0.1:8000
```

Swagger

```
http://127.0.0.1:8000/docs
```

---

## ▶ Run Frontend

```bash
streamlit run frontend/app.py
```

---

## 💬 Workflow

1. Upload one or more PDF documents.
2. Documents are split into text chunks.
3. Chunks are converted into embeddings.
4. Embeddings are stored in a FAISS vector database.
5. Relevant chunks are retrieved based on the user's query.
6. Google Gemini generates an answer using the retrieved context.
7. The answer and source pages are displayed in the chat interface.

---

## 🧠 Architecture

```text
                User

                  │

                  ▼

          Streamlit Frontend

                  │

             HTTP Requests

                  │

                  ▼

            FastAPI Backend

                  │

      ┌───────────┴───────────┐

      ▼                       ▼

 PDF Processing          User Question

      │                       │

      ▼                       ▼

 Text Splitting         Vector Retrieval

      │                       │

      ▼                       ▼

 Sentence Embeddings     Relevant Chunks

      │                       │

      └───────────┬───────────┘

                  ▼

          Google Gemini LLM

                  │

                  ▼

        Final Answer + Sources
```

---

## 📸 Screenshots

Add screenshots here after deployment.

- Home Page
- Upload PDFs
- Chat Interface
- Answer with Sources

---

## 🔮 Future Improvements

- Docker support
- Authentication
- Persistent document management
- Conversation memory
- Streaming responses
- Citation highlighting
- Cloud deployment

---

## 👨‍💻 Author

**Gauransh Chauhan**

GitHub: https://github.com/GauranshChauhan123

---

## ⭐ If you found this project useful, consider giving it a star!