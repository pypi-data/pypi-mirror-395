import typer
import os
import json
from neuroshard.core.store import LocalStore
from neuroshard.core.chunker import decompress_chunk

app = typer.Typer()

@app.callback(invoke_without_command=True)
def checkout(manifest_file: str):
    """Restore a file from its manifest file."""
    if not manifest_file.endswith(".shard.json"):
        typer.echo("Error: Input must be a .shard.json manifest file.")
        raise typer.Exit(code=1)
        
    if not os.path.exists(manifest_file):
        typer.echo(f"Error: Manifest file {manifest_file} not found.")
        raise typer.Exit(code=1)
        
    with open(manifest_file, "rb") as f:
        manifest = json.load(f)
        
    store = LocalStore()
    original_path = manifest["file_path"]
    typer.echo(f"Restoring {original_path}...")
    
    with open(original_path, "wb") as f:
        for block in manifest["blocks"]:
            try:
                compressed = store.read_object(block["hash"])
                data = decompress_chunk(compressed)
                f.write(data)
            except FileNotFoundError:
                typer.echo(f"Error: Block {block['hash']} missing locally.")
                typer.echo("Try running: nshard pull " + manifest_file + " --remote <url>")
                raise typer.Exit(code=1)
                
    typer.echo("Done.")
