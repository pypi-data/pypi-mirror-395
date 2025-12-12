import typer
from neuroshard.commands import (
    init, track, commit, checkout, status, diff, gc, push, pull, git_init
)

app = typer.Typer(help="NeuroShard: Git for AI models.")

app.add_typer(init.app, name="init")
app.add_typer(track.app, name="track")
app.add_typer(commit.app, name="commit")
app.add_typer(checkout.app, name="checkout")
app.add_typer(status.app, name="status")
app.add_typer(diff.app, name="diff")
app.add_typer(gc.app, name="gc")
app.add_typer(push.app, name="push")
app.add_typer(pull.app, name="pull")
app.add_typer(git_init.app, name="git-init")

if __name__ == "__main__":
    app()
