import faiss
import numpy as np
import pickle
import os
from openai import OpenAI

client = OpenAI()

INDEX_PATH = "vector_index.faiss"
META_PATH = "vector_meta.pkl"

def create_index(dim: int):
    index = faiss.IndexFlatL2(dim)  
    meta = []  
    return index, meta

def save_index(index, meta):
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(meta, f)

def load_index():
    if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
        index = faiss.read_index(INDEX_PATH)
        with open(META_PATH, "rb") as f:
            meta = pickle.load(f)
        return index, meta
    return None, None

def add_vectors(index, meta, vectors, chunks):
    vecs_np = np.array(vectors).astype("float32")
    index.add(vecs_np)
    meta.extend(chunks)
    save_index(index, meta)

def search_index(index, meta, query, top_k=5):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    query_vector = response.data[0].embedding
    import numpy as np
    query_vector_np = np.array([query_vector], dtype="float32")
    _, indices = index.search(query_vector_np, top_k)
    results = []
    for idx in indices[0]:
        if idx < len(meta):
            results.append(meta[idx])
    return results

def clear_index():
    if os.path.exists(INDEX_PATH):
        os.remove(INDEX_PATH)
    if os.path.exists(META_PATH):
        os.remove(META_PATH)