import pandas as pd
import hashlib

REQUIRED_COLUMNS = ["user_id", "event_type", "timestamp"]

def validate_dataframe(df: pd.DataFrame):
    schema_valid = all(col in df.columns for col in REQUIRED_COLUMNS)
    null_pct = df.isnull().mean().mean()
    duplicates = df.duplicated().sum()
    return schema_valid, null_pct, duplicates

def checksum_df(df: pd.DataFrame):
    return hashlib.md5(pd.util.hash_pandas_object(df, index=True).values).hexdigest()
