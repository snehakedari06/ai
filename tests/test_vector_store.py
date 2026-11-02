import pytest
import math
import tempfile
from pathlib import Path
from app.services.embeddings import EmbeddingGenerator
from app.services.vector_store import VectorStore

def test_embeddings_normalized():
    generator = EmbeddingGenerator(dimension=128)
    vector = generator.get_embedding("Test codebase embedding content.")
    assert len(vector) == 128
    
    # Check L2 Normalization (norm should be ~1.0)
    magnitude = math.sqrt(sum(v**2 for v in vector))
    assert abs(magnitude - 1.0) < 1e-5

def test_vector_store_search_and_persistence():
    generator = EmbeddingGenerator(dimension=64)
    # Get vectors
    v1 = generator.get_embedding("Authentication login handler method.")
    v2 = generator.get_embedding("Docker build instructions.")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        db_file = Path(tmpdir) / "test_db.json"
        store = VectorStore(db_path=str(db_file))
        
        chunks = [
            {
                "chunk_id": "auth.py#0",
                "file_path": "auth.py",
                "file_type": "source",
                "content": "Authentication login handler method.",
                "embedding": v1
            },
            {
                "chunk_id": "Dockerfile#0",
                "file_path": "Dockerfile",
                "file_type": "configuration",
                "content": "Docker build instructions.",
                "embedding": v2
            }
        ]
        
        store.add_chunks(chunks)
        store.save()
        
        # Reload in a clean store
        new_store = VectorStore(db_path=str(db_file))
        new_store.load()
        assert len(new_store.chunks) == 2
        
        # Test query matching "login callback auth"
        q_vec = generator.get_embedding("login callback auth")
        matches = new_store.search(q_vec, top_k=1)
        assert len(matches) == 1
        assert matches[0]["file_path"] == "auth.py"
        
        # Test file_type filtering
        matches_filtered = new_store.search(q_vec, top_k=2, file_type="configuration")
        assert len(matches_filtered) == 1
        assert matches_filtered[0]["file_path"] == "Dockerfile"
