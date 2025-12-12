import unittest
import os
import shutil
import json
from typer.testing import CliRunner
from neuroshard.cli import app

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.test_dir = "test_env_int"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_cwd)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_full_local_flow(self):
        # 1. Init
        result = self.runner.invoke(app, ["init"])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(os.path.exists(".shard"))

        # 2. Create file
        with open("data.txt", "w") as f:
            f.write("Hello World" * 1000)
        
        # 3. Track
        result = self.runner.invoke(app, ["track", "data.txt"])
        self.assertEqual(result.exit_code, 0)

        # 4. Commit
        result = self.runner.invoke(app, ["commit", "-m", "init"])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(os.path.exists("data.txt.shard.json"))

        # 5. Modify
        with open("data.txt", "w") as f:
            f.write("Modified content")
        
        # 6. Status
        result = self.runner.invoke(app, ["status"])
        self.assertIn("M data.txt", result.stdout)

        # 7. Checkout (Revert)
        result = self.runner.invoke(app, ["checkout", "data.txt.shard.json"])
        self.assertEqual(result.exit_code, 0)
        
        with open("data.txt", "r") as f:
            content = f.read()
            self.assertTrue(content.startswith("Hello World"))

if __name__ == "__main__":
    unittest.main()
