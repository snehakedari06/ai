import time
import logging
from app.inference.base import BaseModel

logger = logging.getLogger("aevor-ai")

class DummyModel(BaseModel):
    """
    A concrete dummy model implementation for initial testing and Phase 1 verification.
    """

    def __init__(self):
        self._loaded = False

    def load(self) -> None:
        logger.info("Initializing DummyModel loader...")
        # Simulate quick initialization delay
        time.sleep(0.05)
        self._loaded = True
        logger.info("DummyModel loaded successfully.")

    def predict(self, text: str, options: dict) -> dict:
        if not self._loaded:
            raise RuntimeError("Model is not loaded.")
        
        # Simple simulated delay and response formatting
        start_time = time.time()
        time.sleep(0.01)
        latency_ms = int((time.time() - start_time) * 1000)

        # Detect RAG prompt and extract user query
        if "Query:" in text and "Context:" in text:
            query = ""
            for line in text.split("\n"):
                if line.strip().startswith("Query:"):
                    query = line.replace("Query:", "").strip()
                    break
            result = f"Grounded response answering: '{query}' based on retrieved codebase context."
        else:
            result = f"Mock inference response for input: {text}"

        return {
            "result": result,
            "metadata": {
                "model": "dummy-model",
                "latency_ms": max(1, latency_ms)
            }
        }

    @property
    def is_ready(self) -> bool:
        return self._loaded
