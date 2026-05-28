from __future__ import annotations

from typing import Any

import pandas as pd


def generate_insights(df: pd.DataFrame, dashboard_payload: dict[str, Any]) -> list[str]:
    insights: list[str] = []

    dead_stock = dashboard_payload.get("dead_stock", [])
    for item in dead_stock[:3]:
        product_name = item.get("product_name", "Unknown Product")
        days_without_sales = item.get("days_since_last_sale", "many")
        insights.append(
            f"WARNING: {product_name} is dead stock with no sales for {days_without_sales} days."
        )

    category_distribution = dashboard_payload.get("category_distribution", [])
    if category_distribution:
        top_category = max(category_distribution, key=lambda item: item.get("total_profit", 0))
        category_name = top_category.get("category", "Unknown")
        insights.append(f"TREND: {category_name} is currently the most profitable category.")

    low_performing_products = dashboard_payload.get("low_performing_products", [])
    loss_products = [
        item for item in low_performing_products if float(item.get("total_profit", 0) or 0) < 0
    ]
    for item in loss_products[:3]:
        product_name = item.get("product_name", "Unknown Product")
        total_loss = round(float(item.get("total_profit", 0)), 2)
        insights.append(f"ALERT: {product_name} is making a loss ({total_loss}).")

    if not df.empty:
        sales_by_product = (
            df.groupby("product_name", as_index=False)["quantity"]
            .sum()
            .sort_values("quantity", ascending=False)
        )
        if not sales_by_product.empty:
            # Use a high quantile to flag unusually strong demand as a spike signal.
            spike_threshold = sales_by_product["quantity"].quantile(0.9)
            spike_df = sales_by_product[sales_by_product["quantity"] >= spike_threshold].head(1)
            if not spike_df.empty:
                spike_row = spike_df.iloc[0]
                insights.append(
                    f"SPIKE: {spike_row['product_name']} shows strong demand with quantity {round(float(spike_row['quantity']), 2)}."
                )

    if not insights:
        insights.append("INFO: No major risk or anomaly detected in the latest dataset.")

    return insights
