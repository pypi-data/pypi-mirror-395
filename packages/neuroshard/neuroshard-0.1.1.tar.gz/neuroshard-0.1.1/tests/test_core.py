import unittest
import os
import shutil
import json
from neuroshard.core.chunker import chunk_file, decompress_chunk
from neuroshard.core.store import LocalStore
from neuroshard.core.manifest import create_manifest

class TestCore(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_env_core"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_cwd)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_chunking_and_hashing(self):
        # Create a dummy file
        content = b"Hello World" * 1000
        with open("test.txt", "wb") as f:
            f.write(content)
            
        blocks = chunk_file("test.txt")
        self.assertTrue(len(blocks) > 0)
        
        # Verify reconstruction
        reconstructed = b""
        for block in blocks:
            reconstructed += decompress_chunk(block["data"])
            
        self.assertEqual(content, reconstructed)

    def test_local_store(self):
        store = LocalStore()
        store.init()
        
        data = b"compressed_data"
        h = "hash123"
        
        store.write_object(h, data)
        self.assertTrue(store.has_object(h))
        self.assertEqual(store.read_object(h), data)

    def test_manifest_creation(self):
        blocks = [{"hash": "h1", "size": 10, "data": b"d1"}]
        meta = {"msg": "test"}
        mhash, manifest, _ = create_manifest("file.txt", blocks, meta)
        
        self.assertEqual(manifest["file_path"], "file.txt")
        self.assertEqual(manifest["blocks"][0]["hash"], "h1")
        self.assertNotIn("data", manifest["blocks"][0])

if __name__ == "__main__":
    unittest.main()
