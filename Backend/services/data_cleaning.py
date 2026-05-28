from __future__ import annotations

from typing import Any

import pandas as pd

CRITICAL_COLUMNS = ["product_name", "date"]
PRICE_COLUMNS = ["cost_price", "selling_price"]


def clean_retail_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    if df.empty:
        raise ValueError("Uploaded file contains no data rows.")

    cleaned_df = df.copy()
    warnings: list[str] = []
    input_rows = int(len(cleaned_df))

    for text_column in ["product_name", "category"]:
        cleaned_df[text_column] = (
            cleaned_df[text_column]
            .astype("string")
            .str.strip()
            .replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})
        )

    rows_before_critical_drop = len(cleaned_df)
    cleaned_df = cleaned_df.dropna(subset=CRITICAL_COLUMNS)
    dropped_critical = int(rows_before_critical_drop - len(cleaned_df))
    if dropped_critical > 0:
        warnings.append(
            f"Dropped {dropped_critical} rows due to missing Product Name or Date."
        )

    cleaned_df["date"] = pd.to_datetime(cleaned_df["date"], errors="coerce")
    cleaned_df["category"] = cleaned_df["category"].fillna("Uncategorized")

    for numeric_column in ["cost_price", "selling_price", "quantity"]:
        cleaned_df[numeric_column] = pd.to_numeric(cleaned_df[numeric_column], errors="coerce")

    # Fill missing prices using product medians, then category medians, then global median.
    for price_column in PRICE_COLUMNS:
        missing_before_fill = int(cleaned_df[price_column].isna().sum())
        if missing_before_fill == 0:
            continue

        cleaned_df[price_column] = cleaned_df[price_column].fillna(
            cleaned_df.groupby("product_name")[price_column].transform("median")
        )
        cleaned_df[price_column] = cleaned_df[price_column].fillna(
            cleaned_df.groupby("category")[price_column].transform("median")
        )
        cleaned_df[price_column] = cleaned_df[price_column].fillna(cleaned_df[price_column].median())

        missing_after_fill = int(cleaned_df[price_column].isna().sum())
        filled_count = missing_before_fill - missing_after_fill
        if filled_count > 0:
            warnings.append(
                f"Filled {filled_count} missing {price_column} values with median-based defaults."
            )

    cleaned_df["quantity"] = cleaned_df["quantity"].fillna(0)

    # Keep loss rows (selling < cost) but remove structurally invalid rows.
    invalid_mask = (
        cleaned_df["date"].isna()
        | cleaned_df["quantity"].le(0)
        | cleaned_df["cost_price"].isna()
        | cleaned_df["selling_price"].isna()
        | cleaned_df["cost_price"].lt(0)
        | cleaned_df["selling_price"].le(0)
    )
    dropped_invalid = int(invalid_mask.sum())
    if dropped_invalid > 0:
        warnings.append(
            f"Dropped {dropped_invalid} invalid rows (bad date, quantity, or price values)."
        )

    cleaned_df = cleaned_df.loc[~invalid_mask].copy()
    cleaned_df["product_name"] = cleaned_df["product_name"].astype(str).str.strip()
    cleaned_df["category"] = (
        cleaned_df["category"]
        .astype(str)
        .str.strip()
        .replace("", "Uncategorized")
    )

    if cleaned_df.empty:
        raise ValueError("No valid rows remain after cleaning the uploaded file.")

    cleaned_df = cleaned_df.sort_values("date").reset_index(drop=True)

    cleaned_rows = int(len(cleaned_df))
    dropped_rows = int(input_rows - cleaned_rows)
    summary: dict[str, Any] = {
        "input_rows": input_rows,
        "cleaned_rows": cleaned_rows,
        "dropped_rows": dropped_rows,
        "warnings": warnings,
    }
    return cleaned_df, summary
