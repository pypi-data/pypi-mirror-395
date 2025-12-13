import typer,mariadb
from pathlib import Path
from rich.live import Live
from rich.table import Table
from ..utils.utils import load_config,echo,build_insert_query
from ..utils.parse_utils import get_file_generator,parse_csv_columns,convert_row
from ..utils.db_utils import mariadb_connect


app = typer.Typer()
APP_DIR = typer.get_app_dir("mob-tfm")
CONFIG_FILE = Path(APP_DIR) / "config.json"
config = load_config(CONFIG_FILE)

@app.command()
def parse( file: Path,
            user: str = typer.Option(config["user"]["name"],"--user","-u", help="Database user name", rich_help_panel="Database Connection"),
            password: str = typer.Option(config["user"]["password"], "--password","-P", help="Database user password", rich_help_panel="Database Connection"),
            database: str = typer.Option(config["user"]["database"],"--database","-d", help="Database name", rich_help_panel="Database Connection"),
            table: str = typer.Option(config["user"]["table"], "--table","-t", help="The Database Table to target", rich_help_panel="Database Connection"),
            host: str = typer.Option(config["user"]["host"], "--host","-h" ,help="The Databse host", rich_help_panel="Database Connection"),
            port: int = typer.Option(config["user"]["port"], "--port", "-p",help="The database port", rich_help_panel="Database Connection"),
            rows: int = typer.Option(config["parse"]["rows"], "--rows", "-r" ,help="Number of rows to read (can be negative)", rich_help_panel="Filling parameters"),
            preview_only: bool = typer.Option(False, help="If --preview tfm won't to fill the table, only preview them", rich_help_panel="Filling parameters")        
):
    """
    fill a mariaDB/MySQL database table with data contained in a csv file.
    """
    if not user:
        echo("The provided user name is empty.\nTFM will continue due to mariadb/mysql allowing empty user names.", mode="warning")
    if not database:
        echo("The provided database name is empty.\nTFM will not be able to connect to the database.", mode="error")
        raise typer.Exit(code=1)
    if not table:
        echo("The provided table name is empty.\nTFM will not be able to insert data into the database.", mode="error")
        raise typer.Exit(code=1)
    if not file.exists():
        echo(f"{file} is not a file path on your system","error")
        raise typer.Exit(code=1)
    if file.suffix != ".csv":
        echo(f"Expected a path to a csv file, received {file} lead to a {file.suffix} file","error")
        raise typer.Exit(code=1)



    file_generator = get_file_generator(file)
    columns = next(file_generator)
    columns_names,converters = parse_csv_columns(columns)


    if preview_only == True:
        echo("[blue bold]preview-only[/blue bold] mode as been detected, skipping table filling","info")
        preview_table = Table("row",*columns_names,title=table,show_lines=True,highlight=True)
        try:
            with Live(preview_table):
                count = 1
                # if rows is positive we loop until our count reach it, if rows is negative we never stop
                
                while count <= rows or rows < 0:
                    row = next(file_generator)
                    preview_table.add_row(f"{count}",*row)
                    count += 1
        except StopIteration:
            echo("Hit maximum rows contained in file !","info")
        finally:
            row_number = count - 1
            echo(f"Finshed. Read {row_number}/{rows} lines","success")
            raise typer.Exit()

    conn_params = {"host":host,
                   "user":user,
                   "password":password,
                   "database":database,
                   "port":port}
    
    conn,cursor = mariadb_connect(**conn_params)

    echo(f"Connection to {database} established","success")
    preview_table = Table("row",*columns_names,title=table,show_lines=True,highlight=True)
    exit_code = 0
    try:
        insert_query = build_insert_query(columns_names,table)
        with Live(preview_table):
            count = 1
            # if rows is positive we loop until our count reach it, if rows is negative we never stop
            
            while count <= rows or rows < 0:
                row = next(file_generator)

                insert_values = convert_row(row,converters)
                cursor.execute(insert_query, insert_values)
                conn.commit()

                preview_table.add_row(f"{count}",*row)
                count += 1
                row_number = count - 1
    except StopIteration:
        echo("Hit maximum rows contained in file !","info")
    except mariadb.Error as error:
        echo(f"Unable to insert data on row {row_number}:\n{error}","error")
        conn.rollback()
        exit_code = 1
    except Exception as error:
        echo(f"Something went wrong while reading/converting file data on row {row_number}:\n{error}","error")
        conn.rollback()
        exit_code = 1
    finally:
        if exit_code == 0:
            echo(f"Finished, Inserted {row_number}/{rows} rows","success")
            echo(f"Last Inserted ID: {cursor.lastrowid}","success")
        conn.close()
        echo("Connection closed","success")
        cursor.close()
        echo("All Ressources have been releashed","success")
        raise typer.Exit(exit_code)

        

