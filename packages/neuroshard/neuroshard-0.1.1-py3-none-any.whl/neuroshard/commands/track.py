import typer
import os
from neuroshard.core.index import Index

app = typer.Typer()

@app.callback(invoke_without_command=True)
def track(path: str):
    """Start tracking a file."""
    if not os.path.exists(path):
        typer.echo(f"Error: File {path} not found.")
        raise typer.Exit(code=1)
    
    index = Index()
    index.add(path)
    typer.echo(f"Tracking {path}")
