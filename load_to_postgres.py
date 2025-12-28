import pandas as pd
import psycopg2
import logging
from dotenv import load_dotenv
import os

load_dotenv()
logging.basicConfig(level=logging.INFO)

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "ops_analytics"),
    "user": os.getenv("POSTGRES_USER", "ops_user"),
    "password": os.getenv("POSTGRES_PASSWORD", "ops_password"),
    "host": "localhost",
    "port": 5432,
}

def incremental_load(df, engine, table_name):
    df.to_sql(table_name, engine, if_exists="append", index=False)


def main():
    df = pd.read_csv("raw_data/transformed_events.csv")

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM ops_raw_events;
    """)

    insert_sql = """
        INSERT INTO ops_raw_events
        (source_system, event_timestamp, metric_1, metric_2, metric_3, metadata)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.executemany(insert_sql, df[
        ["source_system", "event_timestamp", "metric_1", "metric_2", "metric_3", "metadata"]
    ].values.tolist())

    conn.commit()
    cursor.close()
    conn.close()

    logging.info("Loaded data into Postgres")

if __name__ == "__main__":
    main()
