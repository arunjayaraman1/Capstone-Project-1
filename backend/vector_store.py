import numpy as np

vector_store = []

def add_embeddings(chunks, embeddings, document_name):
    for chunk, embedding in zip(chunks, embeddings):
        vector_store.append({
            "chunk": chunk,
            "embedding": embedding,
            "document": document_name
        })

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
def search_similar_chunks(query_embedding, top_k=3):
    
    scores = []

    for item in vector_store:
        score = cosine_similarity(query_embedding, item["embedding"])
        scores.append((score, item))

    scores.sort(key=lambda x: x[0], reverse=True)

    return [item for _, item in scores[:top_k]]
