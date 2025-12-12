import pandas as pd
import sqlite3
import os

def load_queries(data_source=None, table=None):
    """Load saved query history or allow empty mode"""

    if not data_source:
        return []  # No DB → fallback to AI generation
    # If a list is passed directly
    if isinstance(data_source, list):
        return data_source

    # CSV support
    if data_source.endswith(".csv"):
        return pd.read_csv(data_source)["query"].dropna().tolist()

    # SQLite support
    if data_source.startswith("sqlite:///"):
        db_path = data_source.replace("sqlite:///", "")
        if not os.path.exists(db_path):
            return []  # No DB available

        conn = sqlite3.connect(db_path)
        df = pd.read_sql(f"SELECT query FROM {table}", conn)
        return df["query"].dropna().tolist()

    return []  # Unsupported type yet — but handled gracefully
