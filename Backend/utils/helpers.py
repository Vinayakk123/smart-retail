from __future__ import annotations

from datetime import date, datetime
from typing import Any

import numpy as np
import pandas as pd

EXPECTED_INPUT_COLUMNS = [
    "Date",
    "Product Name",
    "Category",
    "Cost Price",
    "Selling Price",
    "Quantity",
]

NORMALIZED_COLUMN_ALIASES = {
    "date": "Date",
    "productname": "Product Name",
    "category": "Category",
    "costprice": "Cost Price",
    "sellingprice": "Selling Price",
    "quantity": "Quantity",
    "qty": "Quantity",
}

STANDARDIZED_COLUMN_MAP = {
    "Date": "date",
    "Product Name": "product_name",
    "Category": "category",
    "Cost Price": "cost_price",
    "Selling Price": "selling_price",
    "Quantity": "quantity",
}


def normalize_column_name(column_name: str) -> str:
    return "".join(char.lower() for char in str(column_name) if char.isalnum())


def standardize_input_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_map: dict[str, str] = {}
    mapped_targets: set[str] = set()

    # Map flexible header variants to the strict input schema expected by the ETL.
    for column_name in df.columns:
        normalized_name = normalize_column_name(column_name)
        target_column = NORMALIZED_COLUMN_ALIASES.get(normalized_name)
        if target_column and target_column not in mapped_targets:
            rename_map[column_name] = target_column
            mapped_targets.add(target_column)

    standardized_df = df.rename(columns=rename_map)
    missing_columns = [
        column_name for column_name in EXPECTED_INPUT_COLUMNS if column_name not in standardized_df.columns
    ]
    if missing_columns:
        joined_columns = ", ".join(missing_columns)
        raise ValueError(f"Missing required columns: {joined_columns}")

    standardized_df = standardized_df[EXPECTED_INPUT_COLUMNS].copy()
    standardized_df = standardized_df.rename(columns=STANDARDIZED_COLUMN_MAP)
    return standardized_df


def to_json_value(value: Any) -> Any:
    if pd.isna(value):
        return None
    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y-%m-%d")
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, np.generic):
        return value.item()
    return value


def dataframe_to_records(df: pd.DataFrame) -> list[dict[str, Any]]:
    serializable_df = df.copy()
    datetime_columns = serializable_df.select_dtypes(include=["datetime64[ns]", "datetimetz"]).columns
    for column_name in datetime_columns:
        serializable_df[column_name] = serializable_df[column_name].dt.strftime("%Y-%m-%d")

    serializable_df = serializable_df.where(pd.notna(serializable_df), None)
    records = serializable_df.to_dict(orient="records")
    return [
        {key: to_json_value(value) for key, value in record.items()}
        for record in records
    ]
