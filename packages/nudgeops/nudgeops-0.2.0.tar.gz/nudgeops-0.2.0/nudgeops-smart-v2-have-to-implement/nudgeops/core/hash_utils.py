"""
nudgeops/core/hash_utils.py

Hashing utilities for NudgeOps.
"""

import hashlib
import json
from typing import Any, Union


def compute_hash(data: Union[str, dict, list, Any]) -> str:
    """
    Compute a deterministic hash of data.
    
    Args:
        data: String, dict, list, or other JSON-serializable data
    
    Returns:
        SHA-256 hash as hex string
    """
    if isinstance(data, str):
        content = data
    elif isinstance(data, (dict, list)):
        # Sort keys for deterministic ordering
        content = json.dumps(data, sort_keys=True, default=str)
    else:
        content = str(data)
    
    return hashlib.sha256(content.encode()).hexdigest()
