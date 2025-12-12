import typer
import os
import json
from neuroshard.core.store import LocalStore
from neuroshard.core.chunker import chunk_file

app = typer.Typer()

@app.callback(invoke_without_command=True)
def diff(path: str):
    """Show block-level diff for a file."""
    if not os.path.exists(path):
        typer.echo(f"File {path} not found.")
        return
        
    manifest_path = f"{path}.shard.json"
    if not os.path.exists(manifest_path):
        typer.echo(f"No commit found for {path}.")
        return
        
    with open(manifest_path, "rb") as f:
        manifest = json.load(f)
    
    current_blocks = chunk_file(path)
    old_blocks = manifest["blocks"]
    
    old_hashes = {b["hash"] for b in old_blocks}
    new_hashes = {b["hash"] for b in current_blocks}
    
    common = old_hashes.intersection(new_hashes)
    added = new_hashes - old_hashes
    removed = old_hashes - new_hashes
    
    typer.echo(f"Diff for {path}:")
    typer.echo(f"  Old blocks: {len(old_blocks)}")
    typer.echo(f"  New blocks: {len(current_blocks)}")
    typer.echo(f"  Unchanged:  {len(common)}")
    typer.echo(f"  Added:      {len(added)}")
    typer.echo(f"  Removed:    {len(removed)}")
    
    if len(current_blocks) > 0:
        change_pct = (len(added) / len(current_blocks)) * 100
        typer.echo(f"  Change:     {change_pct:.1f}%")
