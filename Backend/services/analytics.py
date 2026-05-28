from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import numpy as np
import pandas as pd

from utils.helpers import dataframe_to_records


def empty_kpis() -> dict[str, Any]:
    return {
        "total_revenue": 0.0,
        "total_profit": 0.0,
        "total_products": 0,
        "avg_profit_margin": 0.0,
    }


def add_financial_metrics(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()

    metrics_df = df.copy()
    metrics_df["revenue"] = metrics_df["selling_price"] * metrics_df["quantity"]
    metrics_df["profit"] = (metrics_df["selling_price"] - metrics_df["cost_price"]) * metrics_df["quantity"]
    metrics_df["profit_margin"] = np.where(
        metrics_df["revenue"] > 0,
        metrics_df["profit"] / metrics_df["revenue"],
        0.0,
    )
    return metrics_df


def compute_kpis(df: pd.DataFrame) -> dict[str, Any]:
    if df.empty:
        return empty_kpis()

    return {
        "total_revenue": round(float(df["revenue"].sum()), 2),
        "total_profit": round(float(df["profit"].sum()), 2),
        "total_products": int(df["product_name"].nunique()),
        "avg_profit_margin": round(float(df["profit_margin"].mean()), 4),
    }


def compute_sales_trend(df: pd.DataFrame) -> list[dict[str, Any]]:
    if df.empty:
        return []

    trend_df = (
        df.assign(date=df["date"].dt.floor("D"))
        .groupby("date", as_index=False)
        .agg(
            total_revenue=("revenue", "sum"),
            total_profit=("profit", "sum"),
            total_quantity=("quantity", "sum"),
        )
        .sort_values("date")
    )
    trend_df["total_revenue"] = trend_df["total_revenue"].round(2)
    trend_df["total_profit"] = trend_df["total_profit"].round(2)
    trend_df["total_quantity"] = trend_df["total_quantity"].round(2)

    return dataframe_to_records(trend_df)


def compute_top_products(df: pd.DataFrame, limit: int = 5) -> list[dict[str, Any]]:
    if df.empty:
        return []

    top_products_df = (
        df.groupby("product_name", as_index=False)
        .agg(
            total_quantity=("quantity", "sum"),
            total_revenue=("revenue", "sum"),
            total_profit=("profit", "sum"),
            avg_profit_margin=("profit_margin", "mean"),
        )
        .sort_values(["total_quantity", "total_revenue"], ascending=[False, False])
        .head(limit)
    )
    top_products_df["total_quantity"] = top_products_df["total_quantity"].round(2)
    top_products_df["total_revenue"] = top_products_df["total_revenue"].round(2)
    top_products_df["total_profit"] = top_products_df["total_profit"].round(2)
    top_products_df["avg_profit_margin"] = top_products_df["avg_profit_margin"].round(4)

    return dataframe_to_records(top_products_df)


def compute_low_performing_products(df: pd.DataFrame, limit: int = 5) -> list[dict[str, Any]]:
    if df.empty:
        return []

    performance_df = (
        df.groupby("product_name", as_index=False)
        .agg(
            total_quantity=("quantity", "sum"),
            total_revenue=("revenue", "sum"),
            total_profit=("profit", "sum"),
        )
        .sort_values(["total_profit", "total_revenue", "total_quantity"], ascending=[True, True, True])
        .head(limit)
    )
    performance_df["total_quantity"] = performance_df["total_quantity"].round(2)
    performance_df["total_revenue"] = performance_df["total_revenue"].round(2)
    performance_df["total_profit"] = performance_df["total_profit"].round(2)

    return dataframe_to_records(performance_df)


def compute_dead_stock(df: pd.DataFrame, days_without_sales: int = 30) -> list[dict[str, Any]]:
    if df.empty:
        return []

    latest_date = df["date"].max()
    if pd.isna(latest_date):
        return []

    # Dead stock is measured relative to the latest date inside the uploaded dataset.
    threshold_date = latest_date - pd.Timedelta(days=days_without_sales)
    last_sale_df = (
        df.groupby("product_name", as_index=False)
        .agg(last_sold_date=("date", "max"))
        .sort_values("last_sold_date")
    )
    dead_stock_df = last_sale_df[last_sale_df["last_sold_date"] < threshold_date].copy()
    if dead_stock_df.empty:
        return []

    dead_stock_df["days_since_last_sale"] = (latest_date - dead_stock_df["last_sold_date"]).dt.days
    dead_stock_df["last_sold_date"] = dead_stock_df["last_sold_date"].dt.strftime("%Y-%m-%d")

    return dataframe_to_records(dead_stock_df)


def compute_category_distribution(df: pd.DataFrame) -> list[dict[str, Any]]:
    if df.empty:
        return []

    category_df = (
        df.groupby("category", as_index=False)
        .agg(
            total_revenue=("revenue", "sum"),
            total_profit=("profit", "sum"),
            total_quantity=("quantity", "sum"),
        )
        .sort_values("total_revenue", ascending=False)
    )
    category_df["total_revenue"] = category_df["total_revenue"].round(2)
    category_df["total_profit"] = category_df["total_profit"].round(2)
    category_df["total_quantity"] = category_df["total_quantity"].round(2)

    return dataframe_to_records(category_df)


def compute_product_performance(df: pd.DataFrame, limit: int = 50) -> list[dict[str, Any]]:
    if df.empty:
        return []

    product_df = (
        df.groupby(["product_name", "category"], as_index=False)
        .agg(
            total_quantity=("quantity", "sum"),
            total_revenue=("revenue", "sum"),
            total_profit=("profit", "sum"),
        )
        .sort_values(["total_revenue", "total_quantity"], ascending=[False, False])
        .head(limit)
    )

    product_df["total_quantity"] = product_df["total_quantity"].round(2)
    product_df["total_revenue"] = product_df["total_revenue"].round(2)
    product_df["total_profit"] = product_df["total_profit"].round(2)

    return dataframe_to_records(product_df)


def build_dashboard_payload(df: pd.DataFrame) -> dict[str, Any]:
    if df.empty:
        return {
            "kpis": empty_kpis(),
            "sales_trend": [],
            "top_products": [],
            "low_performing_products": [],
            "category_distribution": [],
            "dead_stock": [],
            "insights": [],
        }

    return {
        "kpis": compute_kpis(df),
        "sales_trend": compute_sales_trend(df),
        "top_products": compute_top_products(df),
        "low_performing_products": compute_low_performing_products(df),
        "category_distribution": compute_category_distribution(df),
        "dead_stock": compute_dead_stock(df),
        "insights": [],
    }


def build_report_payload(df: pd.DataFrame) -> dict[str, Any]:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "row_count": int(len(df)),
        "kpis": compute_kpis(df),
        "aggregated_data": {
            "sales_trend": compute_sales_trend(df),
            "category_distribution": compute_category_distribution(df),
            "product_performance": compute_product_performance(df),
        },
        "dead_stock": compute_dead_stock(df),
        "low_performing_products": compute_low_performing_products(df),
    }
