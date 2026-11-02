import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

class VectorStore:
    """
    In-memory vector database with JSON persistence supporting semantic similarity matching.
    """

    def __init__(self, db_path: str = "vector_store.json"):
        self.db_path = Path(db_path)
        self.chunks: List[Dict[str, Any]] = []

    def clear(self) -> None:
        self.chunks.clear()

    def add_chunks(self, new_chunks: List[Dict[str, Any]]) -> None:
        """
        Appends chunks to the in-memory store.
        """
        self.chunks.extend(new_chunks)

    def save(self) -> None:
        """
        Serializes the current index to the JSON database path.
        """
        # Ensure parent directories exist
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(self.chunks, f, indent=2, ensure_ascii=False)

    def load(self) -> None:
        """
        Loads the index database from JSON.
        """
        if self.db_path.exists():
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    self.chunks = json.load(f)
            except Exception:
                self.chunks = []
        else:
            self.chunks = []

    def search(self, query_vector: List[float], top_k: int = 3, file_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Matches query_vector with stored chunks using dot product cosine similarity,
        returning top_k most similar items.
        """
        matches = []
        for chunk in self.chunks:
            # Filter by classification if requested
            if file_type and chunk.get("file_type") != file_type:
                continue

            vector = chunk.get("embedding")
            if not vector or len(vector) != len(query_vector):
                continue

            # Dot product (since vectors are L2-normalized)
            score = sum(q * v for q, v in zip(query_vector, vector))
            
            # Create a search result containing score and basic metadata
            matches.append({
                "chunk_id": chunk["chunk_id"],
                "file_path": chunk["file_path"],
                "file_type": chunk["file_type"],
                "content": chunk["content"],
                "score": round(score, 4)
            })

        # Sort matches by similarity score descending
        matches.sort(key=lambda x: x["score"], reverse=True)
        return matches[:top_k]
