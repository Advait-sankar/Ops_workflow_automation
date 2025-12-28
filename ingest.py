import pandas as pd
import requests
from pathlib import Path
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

RAW_PATH = Path("raw_data/raw_api_dump.csv")

def ingest_from_api():
    logging.info("Attempting API ingestion")
    response = requests.get("https://jsonplaceholder.typicode.com/posts", timeout=10)
    response.raise_for_status()

    data = response.json()[:50]

    rows = []
    for item in data:
        rows.append({
            "source_system": "external_api",
            "event_timestamp": datetime.utcnow(),
            "metric_1": len(item["title"]),
            "metric_2": len(item["body"]),
            "metric_3": item["id"],
            "metadata": str(item)
        })

    df = pd.DataFrame(rows)
    df.to_csv(RAW_PATH, index=False)

    logging.info("API ingestion successful")

def main():
    RAW_PATH.parent.mkdir(exist_ok=True)

    if RAW_PATH.exists():
        logging.info("Raw data already exists. Skipping ingestion.")
        return

    try:
        ingest_from_api()
    except Exception as e:
        logging.error(f"Ingestion failed: {e}")
        raise RuntimeError("No raw data available for pipeline")

if __name__ == "__main__":
    main()
