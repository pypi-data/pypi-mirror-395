import os
import shutil

class LocalStore:
    def __init__(self, root_dir: str = ".shard"):
        self.root_dir = root_dir
        self.objects_dir = os.path.join(root_dir, "objects")
        self.manifests_dir = os.path.join(root_dir, "manifests")

    def init(self):
        """Initialize the storage directories."""
        os.makedirs(self.objects_dir, exist_ok=True)
        os.makedirs(self.manifests_dir, exist_ok=True)

    def has_object(self, obj_hash: str) -> bool:
        """Check if an object exists in the store."""
        path = self._get_object_path(obj_hash)
        return os.path.exists(path)

    def write_object(self, obj_hash: str, data: bytes):
        """Write a compressed object to the store if it doesn't exist."""
        if self.has_object(obj_hash):
            return
        
        path = self._get_object_path(obj_hash)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(data)

    def read_object(self, obj_hash: str) -> bytes:
        """Read a compressed object from the store."""
        path = self._get_object_path(obj_hash)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Object {obj_hash} not found in store.")
        with open(path, "rb") as f:
            return f.read()

    def _get_object_path(self, obj_hash: str) -> str:
        """Get the filesystem path for an object hash (sharded by first 2 chars)."""
        return os.path.join(self.objects_dir, obj_hash[:2], obj_hash)

    def write_manifest(self, manifest_hash: str, data: bytes):
        """Write a manifest file."""
        path = os.path.join(self.manifests_dir, manifest_hash)
        with open(path, "wb") as f:
            f.write(data)
            
    def read_manifest(self, manifest_hash: str) -> bytes:
        """Read a manifest file."""
        path = os.path.join(self.manifests_dir, manifest_hash)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Manifest {manifest_hash} not found.")
        with open(path, "rb") as f:
            return f.read()
