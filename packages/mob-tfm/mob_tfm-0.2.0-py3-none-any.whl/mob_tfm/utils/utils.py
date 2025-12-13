from typing import Literal
from pathlib import Path

def load_config(file_path: Path) -> dict:
    """Load configuration from a JSON file.
    returns an empty config if the file does not exist.
    """
    import json
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        empty_config = {
            "user":{
                "name": "",
                "password": "",
                "database": "",
                "table":"",
                "host": "localhost",
                "port": 3306
            },

            "generate":{
                "optimized": False,
                "rows": 20,
            },

            "parse":{
                "rows": 20
            }
        }
        return empty_config
    

def echo(message: str, mode: Literal["info","success","warning","error"]) -> None:
    """Print a message to the console with a specific format based on the mode."""
    from rich import print as rprint
    
    modes = {
        "info": "[blue bold]::INFO::[/blue bold] ",
        "success": "[green bold]::SUCCESS::[/green bold] ",
        "warning": "[yellow bold]::WARNING::[/yellow bold] ",
        "error": "[red bold]::ERROR::[/red bold] "
    }
    
    prefix = modes[mode]
    rprint(f"{prefix} {message}")


def clean_str(val: str) -> str:
    """
    A fucntion to clean trailing characters from a string
    """
    return val.strip()
    
def is_valid_str(text: str) -> bool:
    """
    return a bool that tells if a string is a valid content for use.
    
    A valid string must NOT check any the following condition:
    - A string that is empty (Eg:`""` is empty, `"n"` and `" "` are not)
    - A string that contains only whitespaces (space, \\t, \\n, \\r, \\f)     
    """
    
    isEmpty = (text == "" or text.isspace())
    isValid = not(isEmpty) # Valid only if it's not empty
    return isValid

def gen_query_placeholder(length: int) -> str:
    """
    Generate a query placeholder based on the provided length parameter
    
    i.e:
    gen_query_placeholder(3) = '(?,?,?)'

    the length must always be positive
    """
    if length < 0:
        raise ValueError(f"The provided Length must be positive, received {length}")

    question_marks = ["?"] * length
    inner_placeholder = ",".join(question_marks)
    full_placeholder = f"({inner_placeholder})"

    return full_placeholder

def gen_columns_placeholder(columns_names: tuple[str,...]) -> str:
    """
    gen the columns placeholder required for the insert query
    """
    clean_columns = [clean_str(col) for col in columns_names]
    inner_columns_placeholder = ",".join(columns_names)
    full_columns_placeholder = f"({inner_columns_placeholder})" 
    return full_columns_placeholder

def build_insert_query(columns_names: tuple[str,...],table: str) -> str:
    """
    Build the insert query string based on a tuple/list of strings

    i.e:
    ```
    build_insert_query(["name","age","address"], "students"):
    ==> INSERT INTO students (name,age,address) VALUES (?,?,?)
    """
    columns_placeholder = gen_columns_placeholder(columns_names)
    query_placeholder = gen_query_placeholder(len(columns_names))

    insert_query = f"INSERT INTO {table} {columns_placeholder} VALUES {query_placeholder}"
    return insert_query