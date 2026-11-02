import os
from pathlib import Path
from typing import List, Dict, Any

class IngestionService:
    """
    Scans a local repository directory, filters files using gitignore rules,
    and classifies them into categories like source, test, documentation, or configuration.
    """

    def __init__(self, root_path: str):
        self.root_path = Path(root_path).resolve()
        self.ignored_dirs = {
            ".git", ".github", ".venv", "venv", "__pycache__", 
            ".pytest_cache", "build", "dist", "node_modules"
        }
        self.ignored_extensions = {
            ".pyc", ".pyo", ".pyd", ".bin", ".pt", ".pth", 
            ".safetensors", ".onnx", ".exe", ".dll", ".so", 
            ".zip", ".tar", ".gz", ".png", ".jpg", ".jpeg", 
            ".gif", ".ico", ".pdf"
        }

    def should_ignore(self, path: Path) -> bool:
        """
        Determines if a file or directory should be ignored during scanning.
        """
        # Ignore hidden files/directories (except standard config files like .env.example)
        if path.name.startswith(".") and path.name not in {".env.example", ".gitignore"}:
            return True
            
        # Check parts of the path for ignored directories
        for part in path.parts:
            if part in self.ignored_dirs:
                return True

        # Check file extension
        if path.is_file() and path.suffix.lower() in self.ignored_extensions:
            return True

        return False

    def classify_file(self, path: Path) -> str:
        """
        Classifies a file based on its naming conventions and extensions.
        """
        name = path.name.lower()
        suffix = path.suffix.lower()

        # Check for test files
        if "test_" in name or "_test" in name or "tests" in path.parts:
            return "test"

        # Check for configuration/metadata first (e.g. requirements.txt should be configuration, not generic documentation)
        config_files = {
            "dockerfile", "docker-compose.yml", "docker-compose.yaml",
            "package.json", "go.mod", "cargo.toml", "requirements.txt",
            "pyproject.toml", "setup.py", ".gitignore", ".env.example"
        }
        if name in config_files:
            return "configuration"

        # Check for documentation
        if suffix in {".md", ".txt", ".rst"}:
            return "documentation"

        if suffix in {".json", ".yml", ".yaml", ".toml", ".ini", ".conf", ".xml"}:
            return "configuration"

        # Check for source code
        source_suffixes = {
            ".py", ".go", ".js", ".ts", ".jsx", ".tsx", 
            ".c", ".cpp", ".h", ".java", ".rs", ".rb", ".php"
        }
        if suffix in source_suffixes:
            return "source"

        return "other"

    def scan(self) -> List[Dict[str, Any]]:
        """
        Scans the root path recursively and returns metadata about ingested files.
        """
        files_metadata = []
        if not self.root_path.exists() or not self.root_path.is_dir():
            raise ValueError(f"Path is not a valid directory: {self.root_path}")

        for root, dirs, files in os.walk(self.root_path):
            # Prune directory search recursively to speed up os.walk
            dirs[:] = [d for d in dirs if d not in self.ignored_dirs and not d.startswith(".")]

            for file_name in files:
                file_path = Path(root) / file_name
                if self.should_ignore(file_path):
                    continue

                classification = self.classify_file(file_path)
                # Skip files classified as 'other' or skipped extensions
                if classification == "other":
                    continue

                try:
                    # Read content
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    relative_path = file_path.relative_to(self.root_path).as_posix()
                    files_metadata.append({
                        "file_path": relative_path,
                        "file_type": classification,
                        "content": content
                    })
                except Exception:
                    # Ignore read failures (e.g. permission issues or binary false classifications)
                    pass

        return files_metadata
