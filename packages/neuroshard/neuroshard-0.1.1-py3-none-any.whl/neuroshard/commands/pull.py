import typer
import json
from neuroshard.core.store import LocalStore
from neuroshard.core.remote import RemoteClient

app = typer.Typer()

@app.callback(invoke_without_command=True)
def pull(manifest_file: str, remote: str = typer.Option(..., help="Remote server URL")):
    """Pull missing blocks for a manifest."""
    if not manifest_file.endswith(".shard.json"):
        typer.echo("Error: Input must be a .shard.json manifest file.")
        raise typer.Exit(code=1)
        
    with open(manifest_file, "rb") as f:
        manifest = json.load(f)
    
    client = RemoteClient(remote)
    store = LocalStore()
    store.init() 
    
    # Download blocks
    typer.echo(f"Fetching blocks for {manifest['file_path']}...")
    for block in manifest["blocks"]:
        h = block["hash"]
        if not store.has_object(h):
            data = client.download_block(h)
            store.write_object(h, data)
            
    typer.echo("All blocks present.")
