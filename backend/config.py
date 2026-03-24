import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data" / "uploads"
VECTORSTORE_DIR = BASE_DIR / "vectorstore"

# Ollama LLM settings
LLM_MODEL = "llama3.2"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# RAG settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K_RESULTS = 3

# API settings
API_HOST = "0.0.0.0"
API_PORT = 8000