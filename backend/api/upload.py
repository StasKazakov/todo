from fastapi import APIRouter, UploadFile
from io import BytesIO
import os

from services.pdf_reader import extract_text_from_pdf
from services.chunker import split_text
from services.embeddings import create_embeddings

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/api/upload")
async def upload_document(file: UploadFile):
    content = await file.read()

    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(BytesIO(content))
    else:
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            text = content.decode("latin1")

    chunks = split_text(text, chunk_size=500, overlap=50)

    vectors = await create_embeddings(chunks)

    print(f"Uploaded file: {file.filename}")
    print(f"Total chunks: {len(chunks)}")
    print(f"Vectors created: {len(vectors)}")

    return {
        "filename": file.filename,
        "chunks": len(chunks),
        "vectors_count": len(vectors)
    }