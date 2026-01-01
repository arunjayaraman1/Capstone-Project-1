from document_loader import load_document
from chunker import chunk_text
from embeddings import create_embedding
from vector_store import add_embeddings
from vector_store import search_similar_chunks
from llm import generate_answer
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "../data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def health_check():
    return {"status": "Backend running"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = load_document(file_path)
    chunks = chunk_text(text)

    embeddings = [create_embedding(chunk) for chunk in chunks]
    # print(f"Embeddings created: {len(embeddings)}")
    # print(f"Chunks: {chunks}")
    # print(f"Embeddings: {embeddings}")
    
    add_embeddings(
        chunks=chunks,
        embeddings=embeddings,
        document_name=file.filename
    )



    return {
    "filename": file.filename,
    "total_chunks": len(chunks),
    "embeddings_created": len(embeddings),
    "message": "Document embedded and stored successfully"
}

class QuestionRequest(BaseModel):
    question: str
    
@app.post("/ask")
async def ask_question(request: QuestionRequest):
    question_embedding = create_embedding(request.question)
    relevant_chunks = search_similar_chunks(question_embedding)

    if not relevant_chunks:
        return {
            "answer": "The answer is not available in the provided documents.",
            "sources": []
        }

    context = "\n\n".join(
        [chunk["chunk"] for chunk in relevant_chunks]
    )

    answer = generate_answer(context, request.question)

    return {
        "answer": answer,
        "sources": list(set([chunk["document"] for chunk in relevant_chunks]))
    }
