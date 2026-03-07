from fastapi import APIRouter, UploadFile
from io import BytesIO
import os

from services.pdf_reader import extract_text_from_pdf
from services.chunker import split_text
from services.embeddings import create_embeddings
from services.vectorstore import create_index, load_index, add_vectors

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/api/upload")
async def upload_document(file: UploadFile):
    content = await file.read()

    if file.filename.endswith(".pdf"):
        pages = extract_text_from_pdf(BytesIO(content))
    else:
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            text = content.decode("latin1")

        pages = [{
            "page": 1,
            "text": text
        }]

    meta_chunks = []

    for page in pages:
        chunks = split_text(page["text"], chunk_size=500, overlap=50)

        for chunk in chunks:
            meta_chunks.append({
                "text": chunk,
                "page": page["page"],
                "section": page["section"]
            })

    vectors = await create_embeddings([c["text"] for c in meta_chunks])

    dim = len(vectors[0])
    index, meta = load_index()
    if index is None:
        index, meta = create_index(dim)

    add_vectors(index, meta, vectors, meta_chunks)

    return {
        "filename": file.filename,
        "chunks": len(meta_chunks),
        "vectors_count": len(vectors)
    }