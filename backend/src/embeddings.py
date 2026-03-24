from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from config import EMBEDDING_MODEL, VECTORSTORE_DIR
import os

# Embedding model load karo
def get_embeddings():
    embeddings = SentenceTransformerEmbeddings(
        model_name=EMBEDDING_MODEL
    )
    return embeddings

# Documents ko vectorstore mein save karo
def store_embeddings(chunks):
    embeddings = get_embeddings()
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(VECTORSTORE_DIR)
    )
    print(f"Vectorstore mein save ho gaye: {len(chunks)} chunks")
    return vectorstore

# Already saved vectorstore load karo
def load_vectorstore():
    embeddings = get_embeddings()
    
    vectorstore = Chroma(
        persist_directory=str(VECTORSTORE_DIR),
        embedding_function=embeddings
    )
    return vectorstore