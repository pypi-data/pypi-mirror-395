import typer
import os
from neuroshard.core.index import Index

app = typer.Typer()

@app.callback(invoke_without_command=True)
def status():
    """Show status of tracked files."""
    index = Index()
    tracked_files = index.load()
    
    if not tracked_files:
        typer.echo("No tracked files.")
        return
        
    typer.echo("Tracked files:")
    for path in tracked_files:
        status = " "
        if not os.path.exists(path):
            status = "D" # Deleted
        elif not os.path.exists(f"{path}.shard.json"):
            status = "?" # Untracked/New
        else:
            status = "M" # Modified (potentially - simplified check)
            
        typer.echo(f" {status} {path}")
