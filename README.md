# Document Question Answering System (RAG)

## Project Overview

This is a Retrieval-Augmented Generation (RAG) system that enables users to upload documents and ask questions based on their content. The system processes documents by chunking them, creating embeddings, and storing them in a vector store. When a question is asked, it retrieves the most relevant document chunks and uses an LLM to generate accurate answers based on the retrieved context.

### Key Features
- Upload and process PDF and TXT documents
- Automatic text chunking with overlap for better context preservation
- Semantic search using embeddings to find relevant document sections
- Question answering powered by OpenAI's GPT model
- Simple web interface for document upload and Q&A

## How to Run

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Backend Setup and Execution

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the `backend` directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

5. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

   The backend will be available at `http://127.0.0.1:8000`

### UI Setup and Execution

1. Navigate to the UI directory (in a new terminal):
   ```bash
   cd ui
   ```

2. Activate the same virtual environment (or create one if needed):
   ```bash
   source ../backend/.venv/bin/activate  # On Windows: ..\backend\.venv\Scripts\activate
   ```

3. Install dependencies (if not already installed):
   ```bash
   pip install -r ../backend/requirements.txt
   ```

4. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

   The UI will open in your browser at `http://localhost:8501`

### Usage
1. Ensure the backend server is running
2. Open the Streamlit UI in your browser
3. Upload a PDF or TXT document
4. Wait for the document to be processed
5. Enter your question and click "Get Answer"

## LLM and Embedding Model

### LLM Model
- **Model**: `gpt-4o-mini` (OpenAI)
- **Purpose**: Generates answers based on retrieved document chunks
- **Configuration**: Temperature set to 0 for consistent, deterministic responses

### Embedding Model
- **Model**: `all-MiniLM-L6-v2` (Sentence Transformers)
- **Purpose**: Creates vector embeddings for document chunks and user questions
- **Characteristics**: 
  - Lightweight and efficient
  - 384-dimensional embeddings
  - Optimized for semantic similarity tasks

## Chunking and Retrieval

### Chunking Strategy
The system uses a simple but effective text chunking approach:
- **Chunk Size**: 2000 characters per chunk
- **Overlap**: 200 characters between consecutive chunks
- **Purpose**: Ensures that important context at chunk boundaries is preserved, preventing information loss when splitting documents

This overlap strategy helps maintain continuity and ensures that concepts spanning multiple chunks can still be retrieved effectively.

### Retrieval Process
1. **Embedding Creation**: When a question is asked, the system creates an embedding vector for the question using the same embedding model.

2. **Similarity Search**: The system uses cosine similarity to compare the question embedding against all stored document chunk embeddings.

3. **Top-K Retrieval**: The top 3 most similar chunks (by default) are retrieved based on their cosine similarity scores.

4. **Context Assembly**: The retrieved chunks are concatenated to form the context that is passed to the LLM.

5. **Answer Generation**: The LLM generates an answer using only the provided context, ensuring responses are grounded in the uploaded documents.

### Vector Store
The system uses an in-memory vector store that stores:
- Document chunks (text)
- Corresponding embeddings (vectors)
- Source document names

**Note**: The current implementation uses an in-memory store, so data is lost when the server restarts. For production use, consider implementing a persistent vector database (e.g., Chroma, Pinecone, or FAISS with disk persistence).
# Capstone-Project-1
