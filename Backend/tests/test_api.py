from __future__ import annotations

import io

from fastapi.testclient import TestClient

from database import clear_transactions
from main import app

client = TestClient(app)


def _upload_csv(content: str):
    return client.post(
        "/upload",
        files={"file": ("retail.csv", io.BytesIO(content.encode("utf-8")), "text/csv")},
    )


def setup_function() -> None:
    clear_transactions()


def test_upload_with_mixed_quality_data_and_dashboard() -> None:
    csv_content = """Date,Product Name,Category,Cost Price,Selling Price,Quantity
2026-01-01,Old Chips,Snacks,10,20,5
2026-01-05,Expired Milk,Dairy,20,30,4
2026-03-30,Festival Biscuits,Snacks,8,18,120
2026-03-31,Festival Biscuits,Snacks,8,18,140
2026-03-31,Discount Rice,Grains,60,50,10
,Broken Entry,Snacks,5,10,5
2026-03-29,Half Data,Beverages,,25,3
2026-03-29,Milk,Dairy,20,,6
2026-03-31,Rice,Grains,40,55,0
"""

    upload_response = _upload_csv(csv_content)
    assert upload_response.status_code == 200

    upload_payload = upload_response.json()
    assert upload_payload["total_rows"] == 9
    assert upload_payload["cleaned_rows"] == 7
    assert upload_payload["dropped_rows"] == 2
    assert len(upload_payload["preview"]) == 7

    dashboard_response = client.get("/dashboard")
    assert dashboard_response.status_code == 200

    dashboard_payload = dashboard_response.json()
    assert dashboard_payload["kpis"]["total_revenue"] > 0
    assert dashboard_payload["kpis"]["total_profit"] != 0

    dead_stock_products = {item["product_name"] for item in dashboard_payload["dead_stock"]}
    assert "Old Chips" in dead_stock_products
    assert "Expired Milk" in dead_stock_products

    insight_text = " ".join(dashboard_payload["insights"])
    assert "Discount Rice" in insight_text
    assert "Festival Biscuits" in insight_text

    report_response = client.get("/report")
    assert report_response.status_code == 200

    report_payload = report_response.json()
    assert report_payload["row_count"] == 7
    assert "sales_trend" in report_payload["aggregated_data"]
    assert "category_distribution" in report_payload["aggregated_data"]


def test_upload_empty_file_returns_400() -> None:
    response = client.post(
        "/upload",
        files={"file": ("empty.csv", io.BytesIO(b""), "text/csv")},
    )
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()


def test_upload_with_missing_required_columns_returns_400() -> None:
    invalid_csv_content = """Date,Category,Cost Price,Selling Price,Quantity
2026-03-01,Snacks,10,20,5
"""

    response = _upload_csv(invalid_csv_content)
    assert response.status_code == 400
    assert "missing required columns" in response.json()["detail"].lower()
