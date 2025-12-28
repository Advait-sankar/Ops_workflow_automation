from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
import requests
import time

from validation import validate_dataframe, checksum_df
from load_to_postgres import incremental_load

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

DATABASE_URL = "postgresql+psycopg2://ops_user:ops_password@postgres:5432/ops_analytics"

app = FastAPI()
engine = None


# ---------- SAFE DB INIT (FIX) ----------
def init_db():
    global engine
    for _ in range(10):  # ~30 sec retry
        try:
            engine = create_engine(DATABASE_URL)
            with engine.begin() as conn:
                conn.execute(text(open("create_table.sql").read()))
            return
        except OperationalError:
            time.sleep(3)
    raise RuntimeError("Postgres not ready after retries")


@app.on_event("startup")
def startup_event():
    init_db()
# --------------------------------------


AIRFLOW_TRIGGER_URL = "http://airflow:8080/api/v1/dags/ops_workflow_automation_dag/dagRuns"
AUTH = ("admin", "admin")


@app.post("/upload")
async def upload_raw_data(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)

    schema_valid, null_pct, dupes = validate_dataframe(df)
    if not schema_valid:
        raise HTTPException(400, "Schema validation failed")

    checksum = checksum_df(df)

    with engine.begin() as conn:
        res = conn.execute(
            text("SELECT 1 FROM dataset_metadata WHERE checksum=:c"),
            {"c": checksum},
        ).fetchone()

        if res:
            return {"status": "duplicate dataset ignored"}

        meta = conn.execute(
            text("""
                INSERT INTO dataset_metadata (filename, version, row_count, checksum)
                VALUES (
                    :f,
                    COALESCE((SELECT MAX(version)+1 FROM dataset_metadata WHERE filename=:f), 1),
                    :r,
                    :c
                )
                RETURNING dataset_id
            """),
            {"f": file.filename, "r": len(df), "c": checksum},
        )

        dataset_id = meta.scalar()

        conn.execute(
            text("""
                INSERT INTO data_quality_metrics
                (dataset_id, null_percentage, duplicate_rows, schema_valid)
                VALUES (:d, :n, :dup, true)
            """),
            {"d": dataset_id, "n": null_pct, "dup": dupes},
        )

    incremental_load(df, "events")

    requests.post(
        AIRFLOW_TRIGGER_URL,
        auth=AUTH,
        json={"conf": {"dataset_id": dataset_id}},
        timeout=5,
    )

    return {"status": "uploaded", "dataset_id": dataset_id}
