from fastapi import APIRouter, Request
from services.vectorstore import load_index, search_index
from openai import OpenAI
import re

router = APIRouter()
client = OpenAI()

@router.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message", "")

    index, meta = load_index()
    if index is None:
        return {"answer": "No documentation uploaded yet.", "sources": []}

    chunks = search_index(index, meta, message, top_k=5)
    
    context_text = "\n\n".join([f"[{i+1}] {c['text']}" for i, c in enumerate(chunks)])
    prompt = f"""
        Answer the question using the context below.
        Cite sources using [number] when relevant.

        Context:
        {context_text}

        Question: {message}

        Answer:
        """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content
    

    matches = re.findall(r"\[(\d+)\]", answer)
    indices = set(int(m) - 1 for m in matches if int(m) <= len(chunks))

    sources = list(dict.fromkeys(
    f'Section "{chunks[i]["section"]}", page {chunks[i]["page"]}'
    for i in indices
    ))

    answer = re.sub(r"\s*\[\d+\]", "", answer).strip()
    return {
        "answer": answer,
        "sources": sources
    }