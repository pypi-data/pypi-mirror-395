import typer
from rich import print as rprint
from rich.panel import Panel
from rich.text import Text

app = typer.Typer()

@app.command()
def version() -> None:
    """
    Show the current version of Mob TFM.
    """
    version_text = Text(justify="center")
    version_text.append("Version: 1.0.0",style="green bold")
    version_text.append("\n")
    version_text.append("Author: Mob (Mobsy,gitmobkab)",style="blue bold")
    version_text.append("\n")
    version_text.append("Date of Creation: 2024-06-01")
    version_panel = Panel(version_text,
                          title="Mob TFM",
                          subtitle="Under The MIT License")

    rprint(version_panel)
    