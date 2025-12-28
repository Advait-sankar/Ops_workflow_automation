import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Ops Data Upload", layout="centered")

RAW_DIR = Path("raw_data")
RAW_DIR.mkdir(exist_ok=True)

st.title("Operations Data Upload")

uploaded_file = st.file_uploader("Upload raw CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.success(f"File uploaded with {len(df)} rows")
    st.dataframe(df.head())

    save_path = RAW_DIR / "raw_api_dump.csv"
    df.to_csv(save_path, index=False)

    st.info("File saved successfully. Ready for pipeline execution.")


import psycopg2

conn = psycopg2.connect(
    host="postgres",
    dbname="ops_analytics",
    user="ops_user",
    password="ops_password"
)


from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://ops_user:ops_password@postgres:5432/ops_analytics"
)

st.header("📊 Data Quality Dashboard")

try:
    df = pd.read_sql("""
        SELECT m.filename, q.null_percentage, q.duplicate_rows, q.checked_at
        FROM data_quality_metrics q
        JOIN dataset_metadata m USING(dataset_id)
        ORDER BY q.checked_at DESC
    """, engine)

    if df.empty:
        st.info("No data yet. Upload a dataset.")
    else:
        st.dataframe(df)

except Exception:
    st.info("No data quality metrics yet. Upload data to initialize.")
