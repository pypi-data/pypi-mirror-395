import mariadb,sys # fuck optimization, this is python not some rust or C plus i suck at coding (Got the joke, C, C++, C plus...)
from ..utils.utils import echo

def mariadb_connect(**conn_params) -> tuple[mariadb.Connection, mariadb.Cursor]:
    """
    A function that connect to mariadb database and return the connection and cursor objects
    
    `conn_params`:
        the mariadb connection arguments

    For now tfm only pass five values to it under a dict
    
    ```
    conn_params = {
    "host":host,
    "user":user,
    "password":password,
    "database":database,
    "port":port
    }
    ```

    Note:

        This function print and stop the current program in case of an error
    """
    conn = None
    cursor = None
    # So you wanna be startin' somethin' ? 
    # you've got to be startin' somethin'
    # (c) Michael Jackson 1983
    try:
        echo("Connecting to MariaDB/MySQL...","info")
        conn = mariadb.connect(**conn_params)
        echo("Connection Successful","success")
        cursor = conn.cursor()
        return (conn, cursor)
    except mariadb.Error as error:
        echo(f"Error connecting to MariaDB/MySql:\n{error}", "error")
        sys.exit(1)