import logging
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from app.services.ingestion import IngestionService
from app.services.chunker import Chunker
from app.services.embeddings import EmbeddingGenerator
from app.services.vector_store import VectorStore
from app.inference.loader import get_model

logger = logging.getLogger("aevor-ai")
router = APIRouter()

# Initialize global vector store, loading existing index if available
vector_store = VectorStore()
vector_store.load()

class IngestRequest(BaseModel):
    path: str = Field(..., description="Absolute local directory path of the repository to ingest.")

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="User question or query about the codebase.")
    top_k: int = Field(default=3, ge=1, le=10, description="Number of context chunks to retrieve.")

@router.post("/repository/ingest", tags=["Repository"])
async def ingest_repository(request: IngestRequest):
    """
    Ingests, chunks, embeds, and indexes a local repository directory.
    """
    logger.info(f"Received request to ingest repository at path: {request.path}")
    try:
        # 1. Scan & Classify
        scanner = IngestionService(request.path)
        files = scanner.scan()
        if not files:
            return JSONResponse(
                status_code=400,
                content={
                    "error": {
                        "code": "INGESTION_FAILED",
                        "message": f"No indexable files found at the target path: {request.path}"
                    }
                }
            )

        # 2. Chunk Files
        chunker = Chunker()
        all_chunks = []
        for file_metadata in files:
            all_chunks.extend(chunker.chunk_file(file_metadata))

        # 3. Generate Embeddings & Add to Store
        embedder = EmbeddingGenerator()
        for chunk in all_chunks:
            chunk["embedding"] = embedder.get_embedding(chunk["content"])

        # 4. Save to Vector Store
        vector_store.clear()
        vector_store.add_chunks(all_chunks)
        vector_store.save()

        logger.info(f"Ingestion successful. Indexed {len(all_chunks)} chunks from {len(files)} files.")
        return {
            "status": "success",
            "chunks_indexed": len(all_chunks),
            "files_scanned": len(files)
        }
    except Exception as e:
        logger.error(f"Failed to ingest repository: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INGESTION_ERROR",
                    "message": f"An error occurred during repository ingestion: {str(e)}"
                }
            }
        )

@router.post("/repository/query", tags=["Repository"])
async def query_repository(request: QueryRequest):
    """
    Retrieves relevant code chunks and generates a grounded codebase Q&A response.
    """
    logger.info(f"Querying repository for: {request.query}")
    try:
        # Load active model first, ensuring it is ready
        try:
            model = get_model()
        except RuntimeError:
            return JSONResponse(
                status_code=503,
                content={
                    "error": {
                        "code": "MODEL_UNAVAILABLE",
                        "message": "AI model is currently unavailable"
                    }
                }
            )

        if not model.is_ready:
            return JSONResponse(
                status_code=503,
                content={
                    "error": {
                        "code": "MODEL_UNAVAILABLE",
                        "message": "AI model is currently unavailable"
                    }
                }
            )

        # 1. Retrieve Matching Chunks
        embedder = EmbeddingGenerator()
        query_vector = embedder.get_embedding(request.query)
        matches = vector_store.search(query_vector, top_k=request.top_k)

        if not matches:
            return {
                "answer": "No relevant repository context could be found to answer this query.",
                "context": []
            }

        # 2. Compile RAG Context
        context_str = ""
        for idx, match in enumerate(matches):
            context_str += f"\nFile #{idx+1}: {match['file_path']} (Type: {match['file_type']})\n"
            context_str += f"Content:\n{match['content']}\n"
            context_str += "-" * 40 + "\n"

        rag_prompt = (
            "You are Aevor AI, a codebase intelligence assistant.\n"
            "Answer the query based ONLY on the following context. "
            "If the context does not contain sufficient details to answer, state that.\n\n"
            f"Context:\n{context_str}\n"
            f"Query: {request.query}\n"
            "Answer:"
        )

        # 3. Model Inference (Grounded Answer)
        response = model.predict(rag_prompt, options={})

        return {
            "answer": response["result"],
            "context": [
                {
                    "file_path": m["file_path"],
                    "file_type": m["file_type"],
                    "content": m["content"],
                    "score": m["score"]
                }
                for m in matches
            ]
        }
    except Exception as e:
        logger.error(f"Error querying repository: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "QUERY_ERROR",
                    "message": f"An error occurred while querying the repository: {str(e)}"
                }
            }
        )
