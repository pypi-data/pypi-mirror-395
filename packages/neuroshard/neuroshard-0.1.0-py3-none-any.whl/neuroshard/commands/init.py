import typer
from neuroshard.core.store import LocalStore

app = typer.Typer()

@app.callback(invoke_without_command=True)
def init():
    """Initialize a new NeuroShard repository."""
    store = LocalStore()
    store.init()
    typer.echo("Initialized empty NeuroShard repository in .shard/")
