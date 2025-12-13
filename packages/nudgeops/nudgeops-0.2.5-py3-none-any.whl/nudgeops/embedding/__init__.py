"""
Embedding infrastructure for semantic loop detection.
"""

from nudgeops.embedding.service import EmbeddingService
from nudgeops.embedding.utils import cosine_similarity, normalize_text, compute_hash

__all__ = [
    "EmbeddingService",
    "cosine_similarity",
    "normalize_text",
    "compute_hash",
]
