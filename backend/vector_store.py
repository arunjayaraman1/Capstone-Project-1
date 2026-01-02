import chromadb
import os
import uuid
from datetime import datetime
import logging

# Set up logging
logger = logging.getLogger(__name__)


chroma_db_path = os.path.join(os.path.dirname(__file__), "chroma_db")
os.makedirs(chroma_db_path, exist_ok=True)

try:
    client = chromadb.PersistentClient(path=chroma_db_path)
    logger.info(f"ChromaDB client initialized at: {chroma_db_path}")
except Exception as e:
    logger.error(f"Failed to initialize ChromaDB client: {e}")
    raise

# Get or create collection
# Collection: "document_chunks"
# - Stores: text chunks, their embeddings, and document metadata
# - Similarity metric: cosine (for semantic similarity search)
try:
    collection = client.get_or_create_collection(
        name="document_chunks",
        metadata={"hnsw:space": "cosine"}  # Use cosine similarity
    )
    logger.info("ChromaDB collection 'document_chunks' ready")
except Exception as e:
    logger.error(f"Failed to create/get ChromaDB collection: {e}")
    raise

def add_embeddings(chunks, embeddings, document_name):
    """
    Add embeddings to ChromaDB collection.
    
    Args:
        chunks: List of text chunks
        embeddings: List of embedding vectors (as lists)
        document_name: Name of the document
    
    Raises:
        Exception: If adding embeddings to ChromaDB fails
    """
    try:
        # Convert embeddings to lists if they're numpy arrays
        embeddings_list = []
        for emb in embeddings:
            if hasattr(emb, 'tolist'):
                embeddings_list.append(emb.tolist())
            else:
                embeddings_list.append(list(emb))
        
        # Prepare IDs with unique identifier to avoid conflicts
        # Using timestamp and UUID to ensure uniqueness
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        ids = [f"{document_name}_{timestamp}_{unique_id}_{i}" for i in range(len(chunks))]
        documents = chunks
        metadatas = [{"document": document_name} for _ in chunks]
        
        # Add to collection
        # ChromaDB stores:
        # - ids: Unique identifiers for each chunk
        # - embeddings: Vector representations (384-dim for all-MiniLM-L6-v2)
        # - documents: Original text chunks
        # - metadatas: Document names and other metadata
        # All data is persisted to disk automatically
        collection.add(
            ids=ids,
            embeddings=embeddings_list,
            documents=documents,
            metadatas=metadatas
        )
        logger.info(f"Successfully added {len(chunks)} chunks for document: {document_name}")
    except Exception as e:
        logger.error(f"Error adding embeddings to ChromaDB: {e}")
        raise

def search_similar_chunks(query_embedding, top_k=3):
    """
    Search for similar chunks in ChromaDB.
    
    Args:
        query_embedding: Query embedding vector (as list or numpy array)
        top_k: Number of results to return
    
    Returns:
        List of dictionaries with 'chunk', 'document', and 'distance' keys
    
    Raises:
        Exception: If querying ChromaDB fails
    """
    try:
        # Convert query embedding to list if it's a numpy array
        if hasattr(query_embedding, 'tolist'):
            query_embedding_list = query_embedding.tolist()
        else:
            query_embedding_list = list(query_embedding)
        
        # Query ChromaDB
        results = collection.query(
            query_embeddings=[query_embedding_list],
            n_results=top_k
        )
        
        # Format results to match the expected structure
        similar_chunks = []
        if results['ids'] and len(results['ids'][0]) > 0:
            for i in range(len(results['ids'][0])):
                similar_chunks.append({
                    "chunk": results['documents'][0][i],
                    "document": results['metadatas'][0][i]["document"],
                    "distance": results['distances'][0][i] if 'distances' in results else None
                })
        
        logger.debug(f"Found {len(similar_chunks)} similar chunks")
        return similar_chunks
    except Exception as e:
        logger.error(f"Error searching ChromaDB: {e}")
        # Return empty list on error to prevent app crash
        return []