import typer
import os

app = typer.Typer()

@app.callback(invoke_without_command=True)
def git_init():
    """Configure Git to ignore .shard but track manifests."""
    gitignore_path = ".gitignore"
    content = "\n# NeuroShard\n.shard/\n!*.shard.json\n"
    
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "a") as f:
            f.write(content)
    else:
        with open(gitignore_path, "w") as f:
            f.write(content)
            
    typer.echo("Updated .gitignore for NeuroShard.")
