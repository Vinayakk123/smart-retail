from __future__ import annotations

from fastapi import APIRouter

from database import fetch_transactions
from schemas import DashboardResponse, KPIResponse, ReportResponse
from services.analytics import build_dashboard_payload, build_report_payload
from services.insights import generate_insights

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard() -> DashboardResponse:
    df = fetch_transactions()
    if df.empty:
        return DashboardResponse(
            kpis=KPIResponse(),
            sales_trend=[],
            top_products=[],
            low_performing_products=[],
            category_distribution=[],
            dead_stock=[],
            insights=["INFO: Upload a file to generate dashboard analytics."],
        )

    payload = build_dashboard_payload(df)
    payload["insights"] = generate_insights(df, payload)
    return DashboardResponse(**payload)


@router.get("/report", response_model=ReportResponse)
def get_report() -> ReportResponse:
    df = fetch_transactions()
    payload = build_report_payload(df)
    return ReportResponse(**payload)
