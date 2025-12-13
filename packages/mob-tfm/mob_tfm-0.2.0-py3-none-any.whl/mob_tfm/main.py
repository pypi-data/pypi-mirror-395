import typer
from .commands import *


app = typer.Typer(no_args_is_help=True, help="A set of tools to quick up MySql/MariaDB table prototyping")
app.add_typer(version_app)
app.add_typer(unspine_app)
app.add_typer(doctor_app)
app.add_typer(parse_app)
app.add_typer(generate_app)
app.add_typer(config_app)
app.add_typer(explain_app)
