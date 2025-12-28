CREATE TABLE IF NOT EXISTS ops_raw_events (
    source_system VARCHAR(50),
    event_timestamp TIMESTAMP,
    metric_1 FLOAT,
    metric_2 FLOAT,
    metric_3 FLOAT,
    metadata TEXT,
    ingestion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dataset_metadata (
    dataset_id SERIAL PRIMARY KEY,
    filename TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS data_quality_metrics (
    id SERIAL PRIMARY KEY,
    dataset_id INT REFERENCES dataset_metadata(dataset_id),
    null_percentage FLOAT,
    duplicate_rows INT,
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

