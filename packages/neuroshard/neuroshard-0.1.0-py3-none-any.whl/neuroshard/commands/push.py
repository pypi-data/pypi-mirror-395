import typer
import os
import json
import hashlib
from neuroshard.core.index import Index
from neuroshard.core.store import LocalStore
from neuroshard.core.remote import RemoteClient

app = typer.Typer()

@app.callback(invoke_without_command=True)
def push(remote: str = typer.Option(..., help="Remote server URL")):
    """Push tracked files to a remote server."""
    index = Index()
    tracked_files = index.load()
    
    if not tracked_files:
        typer.echo("Nothing to push.")
        return

    client = RemoteClient(remote)
    store = LocalStore()
    
    for file_path in tracked_files:
        manifest_path = f"{file_path}.shard.json"
        if not os.path.exists(manifest_path):
            typer.echo(f"Skipping {file_path} (no manifest found, commit first)")
            continue
            
        with open(manifest_path, "rb") as f:
            manifest_bytes = f.read()
            manifest = json.loads(manifest_bytes)
        
        mhash = hashlib.sha256(manifest_bytes).hexdigest()
            
        typer.echo(f"Pushing {file_path}...")
        
        # Upload blocks
        for block in manifest["blocks"]:
            h = block["hash"]
            if not client.has_block(h):
                try:
                    data = store.read_object(h)
                    client.upload_block(h, data)
                except FileNotFoundError:
                     typer.echo(f"Error: Block {h} missing locally, cannot push.")
                     continue
        
        # Upload manifest
        client.upload_manifest(mhash, manifest_bytes)
        typer.echo(f"Pushed {file_path} -> {mhash}")
