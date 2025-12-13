import typer
import json
from pathlib import Path
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich import print as rprint
from mob_tfm.utils.utils import load_config, echo

app = typer.Typer()

APP_DIR = typer.get_app_dir("mob-tfm")
CONFIG_FILE: Path = Path(APP_DIR) / "config.json"


def save_config(config: dict, file_path: Path) -> None:
    """Save configuration to a JSON file."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w') as file:
        json.dump(config, file, indent=4)


def display_config(config: dict) -> None:
    """Display current configuration in a formatted table."""
    table = Table(title="Current Configuration", show_header=True, header_style="bold cyan")
    table.add_column("Section", style="cyan")
    table.add_column("Key", style="magenta")
    table.add_column("Value", style="green")
    
    for section, values in config.items():
        if isinstance(values, dict):
            for key, value in values.items():
                table.add_row(section, key, str(value))
        else:
            table.add_row(section, "-", str(values))
    
    rprint(table)


@app.command()
def config(view: bool = typer.Option(False, "--view","-v", help="View current configuration")) -> None:
    """
    Create or Edit the configuration for better use of tfm.
    """
    # Create config directory if it doesn't exist
    APP_DIR_PATH = Path(APP_DIR)
    APP_DIR_PATH.mkdir(parents=True, exist_ok=True)
    
    # Load existing config or create new one
    config = load_config(CONFIG_FILE)
    
    if view:
        display_config(config)
        return
    
    echo("Welcome to TFM Configuration Setup", mode="info")
    echo("Press Enter to keep the current value or type a new one", mode="info")
    echo("Cancel at anytime with Ctrl+c","info")
    rprint("\n")
    
    # Database User Configuration
    rprint("[bold cyan]=== Database User Configuration ===[/bold cyan]")
    config["user"]["name"] = Prompt.ask(
        "Database user name",
        default=config["user"]["name"]
    )
    config["user"]["password"] = Prompt.ask(
        "Database user password",
        default=config["user"]["password"],
        password=True
    )
    config["user"]["database"] = Prompt.ask(
        "Database name",
        default=config["user"]["database"]
    )
    config["user"]["table"] = Prompt.ask(
        "Database table name",
        default=config["user"]["table"]
    )
    config["user"]["host"] = Prompt.ask(
        "Database host",
        default=config["user"]["host"]
    )
    config["user"]["port"] = int(Prompt.ask(
        "Database port",
        default=str(config["user"]["port"])
    ))
    
    rprint("\n")
    
    # Generate Configuration
    rprint("[bold cyan]=== Generate Configuration ===[/bold cyan]")
    config["generate"]["optimized"] = Confirm.ask(
        "Use optimized generation methods",
        default=config["generate"]["optimized"]
    )
    config["generate"]["rows"] = int(Prompt.ask(
        "Default number of rows to generate",
        default=str(config["generate"]["rows"])
    ))
    
    rprint("\n")
    
    # Parse Configuration
    rprint("[bold cyan]=== Parse Configuration ===[/bold cyan]")
    config["parse"]["rows"] = int(Prompt.ask(
        "Default number of rows to parse",
        default=str(config["parse"]["rows"])
    ))
    
    rprint("\n")
    
    # Save configuration
    if Confirm.ask("Save configuration?", default=True):
        save_config(config, CONFIG_FILE)
        echo(f"Configuration saved to {CONFIG_FILE}", mode="success")
        display_config(config)
    else:
        echo("Configuration not saved", mode="warning")