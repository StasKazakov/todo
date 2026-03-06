from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    print(data)

    message = data.get("message")


    return {
        "answer": f"You asked: {message}",
        "sources": []
    }