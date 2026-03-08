import asyncio
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI

client = OpenAI()
executor = ThreadPoolExecutor() 

def _sync_embedding(chunk: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=chunk
    )
    return response.data[0].embedding

async def create_embeddings(chunks):
    loop = asyncio.get_event_loop()
    tasks = [loop.run_in_executor(executor, _sync_embedding, c) for c in chunks]
    vectors = await asyncio.gather(*tasks)
    print(f"All embeddings done, total chunks: {len(vectors)}")
    return vectors

