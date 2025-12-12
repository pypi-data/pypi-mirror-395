import os
import json
from typing import Set

class Index:
    def __init__(self, root_dir: str = ".shard"):
        self.index_path = os.path.join(root_dir, "index")

    def load(self) -> Set[str]:
        """Load the set of tracked files."""
        if not os.path.exists(self.index_path):
            return set()
        with open(self.index_path, "r") as f:
            return set(json.load(f))

    def save(self, tracked: Set[str]):
        """Save the set of tracked files."""
        with open(self.index_path, "w") as f:
            json.dump(list(tracked), f, indent=2)

    def add(self, file_path: str):
        """Add a file to tracking."""
        tracked = self.load()
        tracked.add(file_path)
        self.save(tracked)

    def remove(self, file_path: str):
        """Remove a file from tracking."""
        tracked = self.load()
        if file_path in tracked:
            tracked.remove(file_path)
            self.save(tracked)
