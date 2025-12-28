import pandas as pd
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)

RAW_PATH = Path("raw_data/raw_api_dump.csv")
TRANSFORMED_PATH = Path("raw_data/transformed_events.csv")

def validate(df):
    assert not df.empty, "Dataset is empty"
    assert df.isnull().sum().sum() == 0, "Null values detected"

def transform(df):
    df["metric_ratio"] = df["metric_1"] / (df["metric_2"] + 1)
    df["processed_at"] = pd.Timestamp.utcnow()
    return df

def main():
    logging.info("Starting transformation job")
    df = pd.read_csv(RAW_PATH)

    validate(df)
    df = transform(df)

    df.to_csv(TRANSFORMED_PATH, index=False)
    logging.info("Transformation completed")

if __name__ == "__main__":
    main()
