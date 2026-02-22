from sqlalchemy import text
from sqlalchemy.engine import Engine
import psycopg2
from psycopg2 import sql
from pathlib import Path
from typing import Optional, Dict, Any, List, Union
import pandas as pd

def execute_sql_query(
    sql_file_path: str,
    engine: Engine,
    identifiers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    fetch: Optional[str] = None,
) -> Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]:
    """
    Execute a SQL file using a SQLAlchemy engine.

    Supports:
    - Optional identifier replacement (e.g., table/schema names)
    - Optional bound parameters
    - Fetching first row, all rows, or no result

    Parameters
    ----------
    sql_file_path : str
        Path to the .sql file.
    engine : sqlalchemy.engine.Engine
        Active SQLAlchemy engine instance.
    identifiers : dict, optional
        Dictionary of placeholders for identifiers (e.g., schema, table names).
    params : dict, optional
        Bound query parameters for safe execution.
    fetch : {"one", "all", None}, optional
        - "one": returns first row as a dict
        - "all": returns all rows as list of dicts
        - None: returns None

    Returns
    -------
    dict or list of dict or None
        Query results depending on `fetch` option.
    """

    sql_text = Path(sql_file_path).read_text()

    # Replace identifiers in SQL
    if identifiers:
        for key, value in identifiers.items():
            sql_text = sql_text.replace(f"{{{{ {key} }}}}", str(value))

    with engine.begin() as conn:
        result = conn.execute(text(sql_text), params or {})

        if fetch == "one":
            return result.mappings().first()
        elif fetch == "all":
            return result.mappings().all()

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

from sqlalchemy import inspect
from sqlalchemy.engine import Engine


def table_exists(engine: Engine, table_name: str, schema: str = "public") -> bool:
    """
    Check if a table exists in the database.

    Parameters
    ----------
    engine : sqlalchemy.engine.Engine
        Active SQLAlchemy engine instance.
    table_name : str
        Name of the table to check.
    schema : str, default "public"
        Schema name where the table should exist.

    Returns
    -------
    bool
        True if the table exists, False otherwise.
    """
    inspector = inspect(engine)
    return inspector.has_table(table_name, schema=schema)


def fetch_table(engine: Engine, table_name: str, schema: str = "public") -> pd.DataFrame:
    """
    Load an entire table from the database into a pandas DataFrame.

    Parameters
    ----------
    engine : sqlalchemy.engine.Engine
        Active SQLAlchemy engine instance.
    table_name : str
        Table name to fetch.
    schema : str, default "public"
        Schema name where the table resides.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing all rows from the table.

    Raises
    ------
    ValueError
        If the table does not exist.
"""
    if not table_exists(engine, table_name, schema):
        raise ValueError(f"Table '{schema}.{table_name}' does not exist.")

    query = f'SELECT * FROM "{schema}"."{table_name}"'
    return pd.read_sql(query, engine)


def bulk_insert_dataframe(
    df: pd.DataFrame,
    engine: Engine,
    table_name: str,
    schema: str = "public",
    if_exists: str = "append"
) -> None:
    """
    Insert a pandas DataFrame into a database table using SQLAlchemy.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame to insert.
    engine : sqlalchemy.engine.Engine
        Active SQLAlchemy engine instance.
    table_name : str
        Target table name.
    schema : str, default "public"
        Target schema name.
    if_exists : {"fail", "replace", "append"}, default "append"
        Behavior when the table already exists.

    Returns
    -------
    None
    """
    df.to_sql(
        name=table_name,
        con=engine,
        schema=schema,
        if_exists=if_exists,
        index=False,
        method="multi"  
    )