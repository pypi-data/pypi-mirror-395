import platform,sys
from typer import Typer,get_app_dir
from rich import print as rprint
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from pathlib import Path


app = Typer()
CONFIG_FILE :Path = Path(get_app_dir("mob-tfm")) / "config.json"

def config_status() -> Text:
    try:
        with open(CONFIG_FILE,"r"):
            return Text(f"Config File Exist in {CONFIG_FILE}",style="green bold")
    except FileNotFoundError:
        return Text(f"Config File Doesn't Exist,\nit's adviced to create through tfm config command",style="red bold")

@app.command()
def doctor() -> None:
    """
    Show information about Mob TFM.
    Can be considered as a 'about' command.
    """
    layout = Layout(name="root")

    layout.split_column(
        Layout(name="header", size=5),
        Layout(name="body",ratio=3)
    )
    layout["body"].split_row(
        Layout(name="description",ratio=3),
        Layout(name="details",ratio=2)
    )


    header = Text("TFM or Table For Mob is a python module to automate database prototyping",justify="center")

    layout["header"].update(
        Panel(header,border_style="green",title="TFM",padding=(1,0))
    )

    description = Text("Current Version: 1.0.0 (stable)\n")
    description.append(f"Dependencies: Rich, Typer, Mariadb\n")
    description.append(f"OS: {platform.system()}\n")
    description.append(f"Python: {platform.python_version()}\n")
    description.append(f"Python Executable Location: {sys.executable}\n")
    description.append(f"Author: Mob\n")
    description.append(f"Powered by: Python, Poetry, Pypi(pip)\n")
    description.append(Text.assemble("Repo: ",("TFM","blue underline link https://github.com/gitmobkab/TFM")))

    description.highlight_regex("[A-Z]*[a-z]*:",style="green")

    layout["description"].update(
        Panel(description,border_style="blue",title="description",padding=(2,2))
    )

    info = Text("Commands:\n")
    info.append_text(Text("\t config\n",style="blue bold"))
    info.append_text(Text("\t version\n",style="blue bold"))
    info.append_text(Text("\t help\n",style="blue bold"))
    info.append_text(Text("\t doctor\n",style="blue bold"))
    info.append_text(Text("\t unspine\n",style="blue bold"))
    info.append_text(Text("\t generate\n",style="blue bold"))
    info.append_text(Text("\t parse\n",style="blue bold"))

    info.append("Config File:\n")
    info.append_text(config_status())

    layout["details"].update(
        Panel(info,title="details",border_style="blue",padding=(3,5))
    )

    rprint(layout)