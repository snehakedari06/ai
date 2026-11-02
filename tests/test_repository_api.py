import pytest
import tempfile
from pathlib import Path
from app.inference.loader import initialize_model
from app.api.routes.repository import vector_store

def test_repository_ingest_and_query(client):
    """
    Test repository ingestion and querying workflow using a temporary mock workspace.
    """
    # Initialize the active inference model
    initialize_model()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create mock directories and files
        src_dir = Path(tmpdir) / "app"
        src_dir.mkdir()
        
        main_py = src_dir / "main.py"
        with open(main_py, "w", encoding="utf-8") as f:
            f.write(
                "def health_check():\n"
                "    return {'status': 'ok'}\n"
            )
            
        readme_md = Path(tmpdir) / "README.md"
        with open(readme_md, "w", encoding="utf-8") as f:
            f.write(
                "# Project Title\n"
                "This is the project overview and main codebase details.\n"
            )
            
        # Ingest the mock repository
        payload_ingest = {"path": tmpdir}
        response_ingest = client.post("/api/v1/repository/ingest", json=payload_ingest)
        assert response_ingest.status_code == 200
        data_ingest = response_ingest.json()
        assert data_ingest["status"] == "success"
        assert data_ingest["chunks_indexed"] >= 2
        assert data_ingest["files_scanned"] == 2
        
        # Query the ingested repository
        payload_query = {
            "query": "Where is the health check definition?",
            "top_k": 2
        }
        response_query = client.post("/api/v1/repository/query", json=payload_query)
        assert response_query.status_code == 200
        data_query = response_query.json()
        assert "answer" in data_query
        assert "context" in data_query
        assert len(data_query["context"]) > 0
        
        # Assert the model correctly returned a grounded mock response
        assert "Where is the health check definition?" in data_query["answer"]
