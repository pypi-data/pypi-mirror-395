import typer
from neuroshard.core.gc import collect_garbage

app = typer.Typer()

@app.callback(invoke_without_command=True)
def gc(dry_run: bool = False):
    """Garbage collect unused blocks."""
    bytes_freed, count = collect_garbage(dry_run=dry_run)
    if dry_run:
        typer.echo(f"Would free {bytes_freed} bytes ({count} objects).")
    else:
        typer.echo(f"Freed {bytes_freed} bytes ({count} objects).")
