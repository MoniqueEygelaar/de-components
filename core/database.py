from sqlalchemy import text
from sqlalchemy.engine import Engine
import psycopg2
from psycopg2 import sql
from pathlib import Path
from typing import Optional, Dict, Any, List, Union

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

    Examples
    --------
    # Fetch single row
    row = execute_sql_query("query.sql", engine, fetch="one")

    # Fetch all rows
    rows = execute_sql_query("query.sql", engine, fetch="all")

    # With bound parameters and identifier substitution
    rows = execute_sql_query(
        "query.sql",
        engine,
        identifiers={"schema": "staging", "table": "users"},
        params={"start_date": "2024-01-01"},
        fetch="all"
    )
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