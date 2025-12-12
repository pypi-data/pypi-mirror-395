import json
import time
import hashlib
from typing import List, Dict, Any, Tuple

def create_manifest(file_path: str, blocks: List[Dict[str, Any]], meta: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    """
    Create a manifest dictionary and compute its hash.
    Returns (manifest_hash, manifest_dict, manifest_bytes).
    """
    # Filter out 'data' from blocks for the manifest
    clean_blocks = [
        {"hash": b["hash"], "size": b["size"]} 
        for b in blocks
    ]

    manifest = {
        "manifest_version": 1,
        "file_path": file_path,
        "blocks": clean_blocks,
        "meta": {
            **meta,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
    }

    # Canonical JSON representation for hashing
    manifest_bytes = json.dumps(manifest, sort_keys=True).encode("utf-8")
    manifest_hash = hashlib.sha256(manifest_bytes).hexdigest()

    return manifest_hash, manifest, manifest_bytes
