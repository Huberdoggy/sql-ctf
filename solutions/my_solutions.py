import sqlite3
from typing import Any

import pandas as pd
from sqlalchemy import create_engine

queries = {
    'boot_errors': """
    SELECT DISTINCT boot_session AS sessions_with_errors
    FROM boot_logs WHERE log_level IN ('ERROR', 'CRITICAL')
    ORDER BY sessions_with_errors DESC
    """,
    'failed_modules': """
    SELECT module_name, COUNT(status) AS failure_count FROM module_events
    WHERE status = 'FAILED'
    GROUP BY module_name HAVING failure_count >= 1
    ORDER BY failure_count DESC
    """,
    'ct_investigation': """
    SELECT DISTINCT events.module_name, codes.severity AS error_severity
    FROM module_events AS events
    INNER JOIN error_codes AS codes
    ON events.module_name = codes.affected_module
    WHERE events.status = 'FAILED' AND
    (error_severity LIKE 'CRIT%' OR error_severity LIKE 'H___')
    ORDER BY error_severity
    """,
    'triple_threat': """
    SELECT me.module_name, COUNT(DISTINCT me.event_id) AS failed_loads,
    COUNT(DISTINCT ec.error_id) AS crit_errors,
    COUNT(DISTINCT mem.mem_id) AS mem_failures
    FROM module_events AS me
    INNER JOIN error_codes AS ec
    ON me.module_name = ec.affected_module
    AND ec.severity LIKE 'CRIT%'
    INNER JOIN memory_events AS mem
    ON me.module_name = mem.requesting_module
    AND mem.allocation_success != 'True'
    WHERE me.status = 'FAILED'
    GROUP BY me.module_name
    HAVING COUNT(DISTINCT me.event_id) > 0
    AND COUNT(DISTINCT ec.error_id) > 0
    AND COUNT(DISTINCT mem.mem_id) > 0
    ORDER BY (COUNT(DISTINCT me.event_id) + COUNT(DISTINCT ec.error_id) +
    COUNT(DISTINCT mem.mem_id)) DESC
    """,
    'temporal_analysis': """
    SELECT DISTINCT module_name FROM module_events as t1
    INNER JOIN system_calls AS t2
    ON t1.module_name = t2.caller_module
    WHERE t1.boot_session IN (2, 3)
    AND t2.return_code < 0
    AND ABS(t1.timestamp - t2.timestamp) < 100
    ORDER BY t1.module_name
    """,
}


def instantiate_db() -> list[Any, list[str]]:
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


def dump_tables(engine, tables: list[str, None]) -> None:
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


def run_query(engine, heading: str = None, **kwargs) -> None:
    """
    Reusable implementation for various challenges - unpack associated keyword args
    values as lookup keys for 'queries' dictionary
    """
    if len(kwargs.items()) == 0:
        print("No key specified to lookup a query.")
        return
        # For now, I'll only ever pass desired dict key/s as kwargs
    try:
        for v in kwargs.values():
            query = queries.get(v, "Not found.")
            df_query = pd.read_sql_query(query, con=engine)
            heading = (
                f"{'-' * 50} {str(v.upper())} {'-' * 50}"
                if not heading
                else heading.upper()  # Defaults to formatted query name
            )
            print(heading)
            print(df_query, end="\n\n")
    except Exception as e:
        print(f"Caught an error - {type(e).__name__}: {str(e)}")
