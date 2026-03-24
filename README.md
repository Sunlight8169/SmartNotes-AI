# 🎓 SmartNotes AI — Your Study Assistant

A RAG-based intelligent document assistant that lets you chat with your PDFs and study notes.

## Features
- Upload any PDF and ask questions in English or Hindi
- Context-aware answers with source page citations
- Built with LLaMA 3.2 running locally — no API key needed
- Clean chat interface

## Tech Stack
- **LLM:** LLaMA 3.2 via Ollama (local)
- **Embeddings:** Sentence Transformers (all-MiniLM-L6-v2)
- **Vector DB:** ChromaDB
- **Framework:** LangChain
- **Backend:** FastAPI
- **Frontend:** Streamlit

## Project Structure
```
SmartNotes AI/
├── backend/
│   ├── src/
│   │   ├── loader.py       # PDF loading and chunking
│   │   ├── embeddings.py   # Vector embeddings
│   │   ├── retriever.py    # Similarity search
│   │   └── chain.py        # RAG chain
│   ├── config.py
│   └── main.py             # FastAPI server
├── frontend/
│   └── app.py              # Streamlit UI
```

## How to Run

### 1. Install Ollama
Download from https://ollama.com and pull the model:
```
ollama pull llama3.2
```

### 2. Backend
```
cd backend
pip install -r requirements.txt
python main.py
```

### 3. Frontend
```
cd frontend
pip install streamlit requests
streamlit run app.py
```

## How it Works
1. Upload a PDF from the sidebar
2. PDF is chunked and stored in ChromaDB as vectors
3. Your question is converted to a vector and similar chunks are retrieved
4. LLaMA 3.2 generates an answer based on retrieved context
5. Answer is shown with source page numbers
