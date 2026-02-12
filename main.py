import sqlite3

import pandas as pd
from sqlalchemy import create_engine


def dump_tables(tables: list[str, None]):
    """
    I preferred to start from scratch, installing pandas and sqlalchemy in order to build
    the db in a more visually appealing manner for initial inspection.
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
        error_class = type(e).__name__
        error_msg = str(e)
        print(f"Error Class: {error_class}")
        print(f"Error Message: {error_msg}")


##########################################################################################

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

# Eventually, might use this to selectively run other tests/imported functions
if __name__ == "__main__":
    dump_tables(tables)
