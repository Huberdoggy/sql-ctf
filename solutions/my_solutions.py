import sqlite3

import pandas as pd
from sqlalchemy import create_engine

queries = {'boot_errors': """
    SELECT DISTINCT log_level, subsystem, message, boot_session
    FROM boot_logs WHERE log_level LIKE 'ERR%' OR log_level LIKE 'CRIT%'
    """}


def instantiate_db():
    """
    PRELIMINARY WORK:
    Set universally applicable viewing preferences; retrieve top-level view of all tables;
    return a list consisting of an engine object and list of tables.
    """
    pd.set_option('display.max_rows', 1000)
    pd.set_option('display.max_columns', 10)
    pd.set_option('display.width', 200)
    db_url = "sqlite:///kernel_logs.db"
    engine = create_engine(db_url)

    # Connect to db & instantiate a cursor object
    conn = sqlite3.connect('kernel_logs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()  # Returns list of tuples
    return [engine, tables]  # Unpack in main.py


def dump_tables(engine, tables: list[str, None]):
    """
    CHALLENGE 1.1:
    I preferred to start from scratch, installing pandas and sqlalchemy in order to render
    the table data in a more visually appealing manner for initial inspection.
    Feel free to remix this and make it your own.
    """
    lst = []
    for index, item in enumerate(tables):
        lst.append(item[0])  # Break up the tuples - 2nd value is null for each of them
    try:
        for t in lst:
            print(f"{'-' * 50} {str(t.upper())} {'-' * 50}")
            query = f"SELECT * FROM {t}"
            df_query = pd.read_sql_query(query, con=engine)
            print(df_query, end="\n\n")
    except Exception as e:
        print(f"Caught an error - {type(e).__name__}: {str(e)}")


def run_query(engine, **kwargs):
    """
    Reusable implementation for various challenges - unpack associated keyword args
    values as lookup keys for 'queries' dictionary
    """
    if len(kwargs.items()) == 0:
        print("No key specified to lookup a query.")
        return
    try:
        for v in kwargs.values():
            query = queries.get(v, "Not found.")
            df_query = pd.read_sql_query(query, con=engine)
            print(df_query)
    except Exception as e:
        print(f"Caught an error - {type(e).__name__}: {str(e)}")
