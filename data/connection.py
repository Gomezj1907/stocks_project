import psycopg2
from config import PASSWORD


def connect_db():
    
    """
    Establishes a connection to the PostgreSQL database using psycopg2.

    Returns
    -------
    psycopg2 connection object or None
        Returns a connection object if the connection is successful, 
        otherwise returns None if an error occurs.

    Raises
    ------
    Exception
        If an error occurs during the connection attempt, it is caught 
        and printed, and the function returns None.
    """

    try:
        con = psycopg2.connect(
            dbname="stocks_analysis",
            user="stocks_user",
            password= PASSWORD,
            port = "5432",
            host="localhost"
        )
        print("Conectado a la base de datos")
        return con
    
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
    
if __name__ == "__main__":
    con = connect_db()
    if con:
        cursor = con.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"PostgreSQL version: {version}")
        cursor.close()
        con.close()