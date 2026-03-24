from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from src.loader import load_and_split_pdf
from src.embeddings import store_embeddings
from src.chain import get_answer
from config import API_HOST, API_PORT, DATA_DIR
import uvicorn
import shutil
import os

app = FastAPI(title="SmartNotes AI API")

# CORS — frontend se baat karne ke liye
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Health check
@app.get("/")
def root():
    return {"status": "SmartNotes AI backend chal raha hai"}

# PDF upload karo
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        # File save karo
        file_path = DATA_DIR / file.filename
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Load + chunk + embed karo
        chunks = load_and_split_pdf(str(file_path))
        store_embeddings(chunks)
        
        return {
            "status": "success",
            "message": f"{file.filename} successfully upload aur process ho gaya",
            "chunks": len(chunks)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Sawaal poocho
@app.post("/ask")
async def ask_question(data: dict):
    try:
        query = data.get("question", "")
        if not query:
            return {"status": "error", "message": "Sawaal khali hai"}
        
        result = get_answer(query)
        return {
            "status": "success",
            "answer": result["answer"],
            "source_pages": result["source_pages"]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host=API_HOST, port=API_PORT, reload=True)