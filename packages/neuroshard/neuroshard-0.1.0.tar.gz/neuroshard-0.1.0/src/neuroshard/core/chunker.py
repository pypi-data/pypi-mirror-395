import hashlib
import zstandard as zstd
from typing import List, Dict, Any

CHUNK_SIZE = 4 * 1024 * 1024  # 4MB

def sha256_bytes(b: bytes) -> str:
    """Compute SHA-256 hash of bytes."""
    return hashlib.sha256(b).hexdigest()

def compress_chunk(chunk: bytes) -> bytes:
    """Compress a chunk using Zstd."""
    cctx = zstd.ZstdCompressor(level=3)
    return cctx.compress(chunk)

def decompress_chunk(compressed_chunk: bytes) -> bytes:
    """Decompress a chunk using Zstd."""
    dctx = zstd.ZstdDecompressor()
    return dctx.decompress(compressed_chunk)

def chunk_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Read a file, split it into chunks, compress them, and compute hashes.
    Returns a list of block metadata (hash, size, compressed_size).
    Does NOT store the chunks; that's the job of the Store.
    """
    blocks = []
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            
            compressed = compress_chunk(chunk)
            h = sha256_bytes(compressed).lower()
            
            blocks.append({
                "hash": h,
                "size": len(chunk),
                "compressed_size": len(compressed),
                "data": compressed  # We return data here so the caller can store it
            })
    return blocks
