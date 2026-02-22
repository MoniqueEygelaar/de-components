from sqlalchemy import text
from sqlalchemy.engine import Engine
from typing import Optional, Any
import psycopg2
from psycopg2 import sql

def execute_sql_query(
    sql_file_path: str,
    engine: Engine,
    fetch_one: bool = False
) -> Optional[Any]:
    """
    Execute a SQL file using a SQLAlchemy engine.

    Parameters
    ----------
    sql_file_path : str
        Path to a .sql file containing the query.
    engine : sqlalchemy.engine.Engine
        Active SQLAlchemy engine instance.
    fetch_one : bool, default False
        If True, returns the first row of the result.

    Returns
    -------
    Optional[Any]
        First row of result if fetch_one=True, otherwise None.
    """

    with engine.begin() as conn:
        with open(sql_file_path, "r") as f:
            query = f.read()

        result = conn.execute(text(query))

        if fetch_one:
            return result.fetchone()

        return None


def copy_csv_to_postgres(
    csv_file_path: str,
    table_name: str,
    connection_params: dict,
    schema: str = "public"
):
    """
    Load data from a CSV file into a PostgreSQL table using the COPY command.

    Parameters
    ----------
    csv_file_path : str
        Path to the CSV file to load.
    table_name : str
        Target PostgreSQL table name.
    connection_params : dict
        Dictionary of psycopg2 connection parameters
        (e.g., dbname, user, password, host, port).
    schema : str, default "public"
        Target schema name.

    Raises
    ------
    psycopg2.DatabaseError
        If the COPY operation fails.
    FileNotFoundError
        If the CSV file does not exist.
    """

    conn = psycopg2.connect(**connection_params)
    cursor = conn.cursor()

    with open(csv_file_path, "r", encoding="utf-8") as f:
        cursor.copy_expert(
            sql.SQL(f"""
                COPY {schema}.{table_name}
                FROM STDIN
                WITH CSV HEADER DELIMITER ',';
            """),
            f
        )

    conn.commit()
    cursor.close()
    conn.close()