"""
nudgeops.core - Core loop detection primitives.
"""

from nudgeops.core.state import StepRecord, DetectionResult
from nudgeops.core.hash_utils import compute_hash
from nudgeops.core.detectors import (
    StutterDetector,
    InsanityDetector,
    PhantomProgressDetector,
    PingPongDetector,
)

__all__ = [
    "StepRecord",
    "DetectionResult",
    "compute_hash",
    "StutterDetector",
    "InsanityDetector",
    "PhantomProgressDetector",
    "PingPongDetector",
]
