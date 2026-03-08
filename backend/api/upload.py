from fastapi import APIRouter, UploadFile
from io import BytesIO
import os
import re

from services.pdf_reader import extract_text_from_pdf
from services.chunker import split_text
from services.embeddings import create_embeddings
from services.vectorstore import create_index, load_index, add_vectors, clear_index

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/api/upload")
async def upload_document(file: UploadFile):

    content = await file.read()

    ext = os.path.splitext(file.filename)[1].lower()

    if ext == ".pdf":
        pages = extract_text_from_pdf(BytesIO(content))
    elif ext in [".txt", ".md"]:
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            text = content.decode("latin1")

        if ext == ".md":
            raw_sections = re.split(r'\n(?=#)', text)
            pages = []
            for i, section in enumerate(raw_sections):
                if section.strip():
                    first_line = section.strip().split("\n")[0].lstrip("#").strip()
                    pages.append({
                        "page": i + 1,
                        "section": first_line or "General",
                        "text": section
                    })
        else:
            section_pattern = re.compile(r'(\d+\.\s+[A-Z][A-Z\s]{2,30}?)(?:\n|$)')
            sections = []
            last_end = 0
            current_section = "General"

            for match in section_pattern.finditer(text):
                if last_end < match.start():
                    sections.append({
                        "page": 1,
                        "section": current_section,
                        "text": text[last_end:match.start()].strip()
                    })
                current_section = match.group(1).strip()
                last_end = match.end()

            sections.append({
                "page": 1,
                "section": current_section,
                "text": text[last_end:].strip()
            })

            pages = [s for s in sections if s["text"]]

    else:
        return {"error": f"Unsupported file format: {ext}"}

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

    clear_index()
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