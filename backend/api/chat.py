from fastapi import APIRouter, Request
from services.vectorstore import load_index, search_index
from openai import OpenAI

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

    context_text = "\n\n".join([c["text"] for c in chunks])
    prompt = f"Answer the question based on the following context:\n{context_text}\n\nQuestion: {message}\nAnswer:"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content

    sources = list(dict.fromkeys([f'Page {r["page"]}' for r in chunks]))

    return {
        "answer": answer,
        "sources": sources
    }