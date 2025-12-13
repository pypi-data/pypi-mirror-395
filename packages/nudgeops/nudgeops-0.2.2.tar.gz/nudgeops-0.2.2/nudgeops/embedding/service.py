"""
Embedding service using FastEmbed with singleton pattern.

Provides fast, local embedding generation using BAAI/bge-small-en-v1.5.
The model is loaded once and reused for all requests.

Performance characteristics:
- First load: 2-5 seconds (downloads ~33MB on first run)
- Per embed: 6-10ms
- Model cached in ~/.cache/fastembed
"""

from __future__ import annotations

import logging
from typing import ClassVar

import numpy as np

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Singleton embedding service using FastEmbed.

    Usage:
        service = EmbeddingService.get_instance()
        embedding = service.embed("search for return policy")

    The service uses BAAI/bge-small-en-v1.5 which produces:
    - 384-dimensional embeddings
    - Optimized for semantic similarity
    - Fast CPU inference via ONNX
    """

    _instance: ClassVar[EmbeddingService | None] = None
    _model: ClassVar = None  # fastembed.TextEmbedding

    def __init__(self) -> None:
        """Private constructor. Use get_instance() instead."""
        pass

    @classmethod
    def get_instance(cls, model_name: str = "BAAI/bge-small-en-v1.5") -> EmbeddingService:
        """
        Get the singleton instance of the embedding service.

        Args:
            model_name: FastEmbed model name. Default is BGE-small-en-v1.5

        Returns:
            Singleton EmbeddingService instance
        """
        if cls._instance is None:
            cls._instance = cls()
            cls._load_model(model_name)
        return cls._instance

    @classmethod
    def _load_model(cls, model_name: str) -> None:
        """
        Load the embedding model.

        This is called once when the singleton is first created.
        """
        try:
            from fastembed import TextEmbedding

            logger.info(f"Loading embedding model: {model_name}")
            cls._model = TextEmbedding(model_name=model_name)
            logger.info("Embedding model loaded successfully")
        except ImportError:
            logger.error(
                "fastembed not installed. Install with: pip install fastembed"
            )
            raise
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise

    def embed(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            384-dimensional numpy array

        Raises:
            RuntimeError: If model is not loaded
        """
        if self._model is None:
            raise RuntimeError("Embedding model not loaded. Call get_instance() first.")

        embeddings = list(self._model.embed([text]))
        return np.array(embeddings[0], dtype=np.float32)

    def embed_batch(self, texts: list[str]) -> list[np.ndarray]:
        """
        Generate embeddings for multiple texts.

        More efficient than calling embed() multiple times due to batching.

        Args:
            texts: List of texts to embed

        Returns:
            List of 384-dimensional numpy arrays
        """
        if self._model is None:
            raise RuntimeError("Embedding model not loaded. Call get_instance() first.")

        if not texts:
            return []

        embeddings = list(self._model.embed(texts))
        return [np.array(e, dtype=np.float32) for e in embeddings]

    @classmethod
    def reset(cls) -> None:
        """
        Reset the singleton instance.

        Useful for testing or when switching models.
        """
        cls._instance = None
        cls._model = None


def get_embedding(text: str, model_name: str = "BAAI/bge-small-en-v1.5") -> list[float]:
    """
    Convenience function to get embedding as a list.

    Args:
        text: Text to embed
        model_name: Model name to use

    Returns:
        384-element list of floats
    """
    service = EmbeddingService.get_instance(model_name)
    embedding = service.embed(text)
    return embedding.tolist()
