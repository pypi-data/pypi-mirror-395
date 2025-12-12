import typer
import os
from neuroshard.core.index import Index
from neuroshard.core.store import LocalStore
from neuroshard.core.chunker import chunk_file
from neuroshard.core.manifest import create_manifest

app = typer.Typer()

@app.callback(invoke_without_command=True)
def commit(message: str = typer.Option(..., "-m", "--message", help="Commit message")):
    """Commit tracked files."""
    index = Index()
    tracked_files = index.load()
    
    if not tracked_files:
        typer.echo("Nothing to commit (no tracked files).")
        return

    store = LocalStore()
    
    for file_path in tracked_files:
        if not os.path.exists(file_path):
            typer.echo(f"Warning: Tracked file {file_path} missing, skipping.")
            continue
            
        typer.echo(f"Chunking {file_path}...")
        blocks = chunk_file(file_path)
        
        # Store blocks
        for block in blocks:
            store.write_object(block["hash"], block["data"])
            
        # Create manifest
        meta = {"message": message}
        mhash, manifest, manifest_bytes = create_manifest(file_path, blocks, meta)
        store.write_manifest(mhash, manifest_bytes)
        
        # Write full manifest to workspace file (Git-friendly)
        manifest_path = f"{file_path}.shard.json"
        with open(manifest_path, "wb") as f:
            f.write(manifest_bytes)
            
        typer.echo(f"Committed {file_path} -> {mhash}")
        typer.echo(f"Updated manifest: {manifest_path}")
