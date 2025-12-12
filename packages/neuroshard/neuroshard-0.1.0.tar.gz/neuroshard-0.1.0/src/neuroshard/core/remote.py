import requests
import os

class RemoteClient:
    def __init__(self, base_url: str, token: str = None):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.session = requests.Session()
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    def has_block(self, obj_hash: str) -> bool:
        """Check if remote has a block."""
        resp = self.session.head(f"{self.base_url}/blocks/{obj_hash}")
        return resp.status_code == 200

    def upload_block(self, obj_hash: str, data: bytes):
        """Upload a block to remote."""
        resp = self.session.put(f"{self.base_url}/blocks/{obj_hash}", data=data)
        resp.raise_for_status()

    def download_block(self, obj_hash: str) -> bytes:
        """Download a block from remote."""
        resp = self.session.get(f"{self.base_url}/blocks/{obj_hash}")
        resp.raise_for_status()
        return resp.content

    def upload_manifest(self, manifest_hash: str, data: bytes):
        """Upload a manifest to remote."""
        resp = self.session.put(f"{self.base_url}/manifests/{manifest_hash}", data=data)
        resp.raise_for_status()

    def download_manifest(self, manifest_hash: str) -> bytes:
        """Download a manifest from remote."""
        resp = self.session.get(f"{self.base_url}/manifests/{manifest_hash}")
        resp.raise_for_status()
        return resp.content
