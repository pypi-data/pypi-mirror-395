import typer,mariadb
from pathlib import Path
from rich.table import Table
from rich.live import Live
from mob_tfm.utils.generate_utils import build_columns,build_faker,run_column_generator
from ..utils.utils import load_config,echo,build_insert_query
from mob_tfm.utils.db_utils import mariadb_connect

app = typer.Typer()
APP_DIR = typer.get_app_dir("mob-tfm")
CONFIG_FILE = Path(APP_DIR) / "config.json"
config = load_config(CONFIG_FILE)


@app.command()
def generate(   format: str,
                seed: int | None = typer.Option(None, "--seed","-s", help="Seed for the random generator.", rich_help_panel="Generation Arguments"),
                user: str = typer.Option(config["user"]["name"], "--user", "-u", help="Database user name.",rich_help_panel="Database Connection"),
                password: str = typer.Option(config["user"]["password"], "--password", "-P", help="Database user password.",rich_help_panel="Database Connection"),
                database: str = typer.Option(config["user"]["database"], "--database", "-d",help="Database name.",rich_help_panel="Database Connection"),
                table: str = typer.Option(config["user"]["table"], "--table", "-t",help="Database table name.",rich_help_panel="Database Connection"),
                host: str = typer.Option(config["user"]["host"], "--host","-h", help="Database host.",rich_help_panel="Database Connection"),
                port: int = typer.Option(config["user"]["port"], "--port", "-p", help="Database port.",rich_help_panel="Database Connection"),
                optimized: bool = typer.Option(config["generate"]["optimized"], help="Use optimized generation methods.",rich_help_panel="Generation Arguments"),
                rows: int = typer.Option(config["generate"]["rows"], "--rows","-r", help="Number of rows to generate.",rich_help_panel="Generation Arguments")
             ):
    """
    fill a mariaDB/MySQL database table with fake data based on a format string.
    """

    if not user:
        echo("The provided user name is empty.\nTFM will continue due to mariadb/mysql allowing empty user names.", mode="warning")
    if not database:
        echo("The provided database name is empty.\nTFM will not be able to connect to the database.", mode="error")
        raise typer.Exit(code=1)
    if not table:
        echo("The provided table name is empty.\nTFM will not be able to insert data into the database.", mode="error")
        raise typer.Exit(code=1)
    
    columns = build_columns(format)
    names = [col.alias for col in columns]
    names = tuple(names)
    fake = build_faker(seed,optimized)
    

    if "" in names:
        echo("Detected empty column Preview only mode enabled.",mode="info")
        preview_table = Table("row",*names,title=table, caption="The World is a cruel thing" ,show_lines=True,highlight=True)
        with Live(preview_table):
            count = 1
            while count <= rows:
                line = []
                for i in range(len(columns)):
                    line.append(run_column_generator(columns[i].generator,fake,**columns[i].args))
                renderable_line = map(str,line)

                preview_table.add_row(f"{count}",*renderable_line)
                count += 1
        raise typer.Exit(0)

    conn_params = {"host":host,
                   "user":user,
                   "password":password,
                   "database":database,
                   "port":port}
    
    conn,cursor = mariadb_connect(**conn_params)

    echo(f"Connection to {database} esthablished","success")
    preview_table = Table("row",*names,title=table, caption="The World is a cruel thing" ,show_lines=True)
    try:
        with Live(preview_table):
            exit_code = 0
            echo("Generating data...",mode="info")
            count = 1
            while count <= rows:
                row = count - 1
                line : list[object] = []
                for i in range(len(columns)):
                    line.append(run_column_generator(columns[i].generator,fake,**columns[i].args))
                insert_query = build_insert_query(names, table)
                cursor.execute(insert_query, line)
                conn.commit()

                renderable_line = map(str,line)
                preview_table.add_row(f"{count}",*renderable_line)
                count += 1
    except mariadb.Error as error:
        echo(f"Error while inserting data on row {row} into the database:\n{error}",mode="error")
        conn.rollback()
        exit_code = 1
    except Exception as error:
        echo(f"Error while generating data on row {row}:\n{error}",mode="error")
        conn.rollback()
        exit_code = 1
    finally:
        if exit_code == 0:
            echo(f"Finished, Inserted {row}/{rows} rows","success")
            echo(f"Last Inserted ID: {cursor.lastrowid}","success")
        conn.close()
        echo("Connection closed","success")
        cursor.close()
        echo("All Ressources have been releashed","success")
        raise typer.Exit(exit_code)