from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from models import DB_COLUMNS, TABLE_NAME

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "smart_retail.db"

_CREATE_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    date TEXT NOT NULL,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    cost_price REAL NOT NULL,
    selling_price REAL NOT NULL,
    quantity REAL NOT NULL,
    revenue REAL NOT NULL,
    profit REAL NOT NULL,
    profit_margin REAL NOT NULL
)
"""


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(_CREATE_TABLE_SQL)
        connection.commit()


def replace_transactions(df: pd.DataFrame) -> None:
    init_db()
    safe_df = df.reindex(columns=DB_COLUMNS).copy()
    safe_df["date"] = pd.to_datetime(safe_df["date"], errors="coerce").dt.strftime("%Y-%m-%d")

    with get_connection() as connection:
        connection.execute(f"DELETE FROM {TABLE_NAME}")
        if not safe_df.empty:
            safe_df.to_sql(TABLE_NAME, connection, if_exists="append", index=False)
        connection.commit()


def fetch_transactions() -> pd.DataFrame:
    init_db()
    query = f"SELECT {', '.join(DB_COLUMNS)} FROM {TABLE_NAME}"

    with get_connection() as connection:
        df = pd.read_sql_query(query, connection)

    if df.empty:
        return df

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    numeric_cols = [
        "cost_price",
        "selling_price",
        "quantity",
        "revenue",
        "profit",
        "profit_margin",
    ]
    for column in numeric_cols:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df.dropna(subset=["date"]).reset_index(drop=True)


def clear_transactions() -> None:
    init_db()
    with get_connection() as connection:
        connection.execute(f"DELETE FROM {TABLE_NAME}")
        connection.commit()
