import typer
from rich import print as rprint
from rich.markdown import Markdown
from rich.console import Console
from importlib import resources
from ..utils.utils import is_valid_str, echo


app = typer.Typer()


def get_available_commands() -> tuple[str, ...]:
	"""Return the list of available command doc names from docs/commands."""
	try:
		commands_dir = resources.files("docs").joinpath("commands")
		names: list[str] = []
		for item in commands_dir.iterdir():
			if item.name.startswith("README.") and item.name.endswith('.md'):
				# README.config.md -> config
				base = item.name[len("README."):-3]
				names.append(base)
		return tuple(sorted(names))
	except Exception:
		return tuple()


@app.command()
def explain(
	commands: str,
	pretty: bool = typer.Option(False,"-p", "--pretty",help="force activation markdown styling/ may cause issue on old terminals")
):
	"""
	Open and page the documentation for one or more commands from `docs/commands/README.<command>.md`.
	"""
	AVAILABLE = get_available_commands()

	for cmd in commands.split():
		if not is_valid_str(cmd):
			bad_command_response(cmd, AVAILABLE)
		try:
			console = Console()
			file = f"README.{cmd}.md"
			file_content = resources.files("docs").joinpath("commands", file).read_text(encoding="utf-8")
			md = Markdown(file_content)
			with console.pager(styles=pretty, links=True):
				console.print(md)
		except FileNotFoundError:
			bad_command_response(cmd, AVAILABLE)


def bad_command_response(command_name: str, available: tuple[str, ...]) -> None:
	"""
	Print that the command is unknown, list known commands and exit the typer app.
	"""
	echo(f"'{command_name}' is not a known tfm command", "error")
	echo("If the specified command is correct, please open an issue on the repo page", "info")
	echo("Available commands:", "info")
	print_help(available)
	raise typer.Abort()


def print_help(available: tuple[str, ...]) -> None:
	"""Print a list of all the known command names."""
	for name in available:
		rprint(f"\t '{name}'")

