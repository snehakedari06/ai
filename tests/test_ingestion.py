import pytest
from pathlib import Path
from app.services.ingestion import IngestionService
from app.services.chunker import Chunker

def test_file_classification():
    service = IngestionService("c:\\aveora")
    assert service.classify_file(Path("main.py")) == "source"
    assert service.classify_file(Path("tests/test_ingestion.py")) == "test"
    assert service.classify_file(Path("README.md")) == "documentation"
    assert service.classify_file(Path("Dockerfile")) == "configuration"
    assert service.classify_file(Path("docker-compose.yml")) == "configuration"
    assert service.classify_file(Path("requirements.txt")) == "configuration"
    assert service.classify_file(Path("unsupported_extension.xyz")) == "other"

def test_should_ignore():
    service = IngestionService("c:\\aveora")
    # Virtual environment checks
    assert service.should_ignore(Path("c:\\aveora\\.venv\\bin\\python")) is True
    # Git folder checks
    assert service.should_ignore(Path("c:\\aveora\\.git\\config")) is True
    # Pycache checks
    assert service.should_ignore(Path("c:\\aveora\\app\\__pycache__\\main.pyc")) is True
    # Valid files checks
    assert service.should_ignore(Path("c:\\aveora\\app\\main.py")) is False
    assert service.should_ignore(Path("c:\\aveora\\.env.example")) is False

def test_chunker_basic():
    chunker = Chunker(chunk_size=10, chunk_overlap=2)
    file_metadata = {
        "file_path": "test.txt",
        "file_type": "documentation",
        "content": "abcdefghijkl" # 12 characters
    }
    chunks = chunker.chunk_file(file_metadata)
    assert len(chunks) > 0
    assert chunks[0]["file_path"] == "test.txt"
    assert chunks[0]["file_type"] == "documentation"
