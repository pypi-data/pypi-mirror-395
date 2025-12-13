import typer
from rich import print as rprint
from rich.markdown import Markdown
from rich.console import Console
from importlib import resources
from ..utils.utils import is_valid_str,echo
from ..utils.generate_utils import GENERATORS


app = typer.Typer()

GENERATORS_NAMES = tuple(GENERATORS.keys())

@app.command()
def unspine(
            generators: str,
            pretty: bool = typer.Option(False,"-p","--pretty",help="force activation markdown styling/ may cause issue on old terminals")
            ):
    """
    'Unspine'/print the doc of a list of tfm generators inside of a pager (alternative screen)
    """
    for generator in generators.split():
        if not is_valid_str(generator):
            bad_generator_response(generator,GENERATORS_NAMES)
        try:
            console = Console()
            file = f"README.{generator}.md"
            file_content = resources.files("docs").joinpath("generators", file).read_text(encoding="utf-8")
            md = Markdown(file_content)        
            with console.pager(styles=pretty,links=True):
                console.print(md)
        except FileNotFoundError:
            bad_generator_response(generator,GENERATORS_NAMES)



def bad_generator_response(generator_name,GENERATORS_NAMES) -> None:
    """
    print that generator_name is unknow, list the know generators and exit the typer app
    """
    echo(f"'{generator_name}' is not a know tfm generator","error")
    echo(f"if the specified tfm generator is indeed correct please open an issue on the repo page","info")
    echo(f"Our team will promptly correct the issue","info")
    print_help(GENERATORS_NAMES)
    raise typer.Abort()


def print_help(GENERATORS_NAMES: tuple[str,...]) -> None:
    """print a list of all the known tfm generators"""
    echo("The available tfm generators on your version are:","info")
    for name in GENERATORS_NAMES:
        rprint(f"\t '{name}'")