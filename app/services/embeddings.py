import re
import math
from typing import List

class EmbeddingGenerator:
    """
    Offline-compatible, deterministic term-frequency hashing embedding generator.
    Produces L2-normalized float vectors of a fixed dimension.
    """

    def __init__(self, dimension: int = 128):
        self.dimension = dimension

    def get_embedding(self, text: str) -> List[float]:
        """
        Generates a deterministic, L2-normalized vector from the input text.
        """
        # Clean text
        text_clean = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
        words = text_clean.split()

        vector = [0.0] * self.dimension
        if not words:
            return vector

        # Term frequency hashing mapping
        for word in words:
            # Simple djb2-like hash mapped to vector space dimension
            h = 5381
            for char in word:
                h = ((h << 5) + h) + ord(char)
            index = abs(h) % self.dimension
            vector[index] += 1.0

        # L2 Normalization (ensures dot product equals cosine similarity)
        magnitude = math.sqrt(sum(v ** 2 for v in vector))
        if magnitude > 0:
            vector = [v / magnitude for v in vector]

        return vector
