from sentence_transformers import SentenceTransformer
import numpy as np

# Load model once (important for performance)
model = SentenceTransformer("all-MiniLM-L6-v2")

def create_embedding(text: str):
    """
    Create embedding for text.
    Returns numpy array (can be converted to list for ChromaDB).
    """
    embedding = model.encode(text)
    return np.array(embedding)
