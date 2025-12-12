import os
import json
from typing import Set
from neuroshard.core.store import LocalStore

def collect_garbage(dry_run: bool = False) -> int:
    """
    Remove objects not referenced by any manifest.
    Returns number of bytes freed.
    """
    store = LocalStore()
    
    # 1. Collect all referenced hashes
    referenced_hashes: Set[str] = set()
    
    if not os.path.exists(store.manifests_dir):
        return 0
        
    for manifest_name in os.listdir(store.manifests_dir):
        try:
            data = store.read_manifest(manifest_name)
            manifest = json.loads(data)
            for block in manifest["blocks"]:
                referenced_hashes.add(block["hash"])
        except Exception:
            continue
            
    # 2. Scan all objects
    freed_bytes = 0
    removed_count = 0
    
    if not os.path.exists(store.objects_dir):
        return 0

    for root, _, files in os.walk(store.objects_dir):
        for filename in files:
            obj_hash = filename
            if obj_hash not in referenced_hashes:
                path = os.path.join(root, filename)
                size = os.path.getsize(path)
                if not dry_run:
                    os.remove(path)
                    # Clean up empty dirs
                    try:
                        os.rmdir(os.path.dirname(path))
                    except OSError:
                        pass
                freed_bytes += size
                removed_count += 1
                
    return freed_bytes, removed_count
