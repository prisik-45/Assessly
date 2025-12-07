from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, Form, Body
import shutil
import os
from pdfminer.high_level import extract_text
from docx import Document
from fastapi.middleware.cors import CORSMiddleware
from src.backend import generate_quiz_from_pdf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def quiz_request(
    num_questions: int = Form(5, ge=1, le=20),
    difficulty: str = Form("medium", regex="^(easy|medium|hard)$")
):
    return {"num_questions": num_questions, "difficulty": difficulty}

def extract_text_from_pdf(file_path: str) -> str:
    return extract_text(file_path)

def extract_text_from_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

@app.post("/upload-n-generate/")
async def generate_quiz(file: UploadFile = File(..., description="Upload PDF or DOCX file"), request: dict = Depends(quiz_request)):
    
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided.")
    
    if not (file.filename.endswith('.pdf') or file.filename.endswith('.docx')):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF or DOCX file.")
    
    temp_path = f"temp_{file.filename}"
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if file.filename.endswith('.pdf'):
            text = extract_text_from_pdf(temp_path)
        else:
            text = extract_text_from_docx(temp_path)
            
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text extracted from file")
        
        response = generate_quiz_from_pdf(text, request["num_questions"], request["difficulty"])
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating quiz: {str(e)}")
    
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)