from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    preview: list[dict[str, Any]] = Field(default_factory=list)
    total_rows: int
    cleaned_rows: int
    dropped_rows: int
    warnings: list[str] = Field(default_factory=list)


class KPIResponse(BaseModel):
    total_revenue: float = 0.0
    total_profit: float = 0.0
    total_products: int = 0
    avg_profit_margin: float = 0.0


class DashboardResponse(BaseModel):
    kpis: KPIResponse
    sales_trend: list[dict[str, Any]] = Field(default_factory=list)
    top_products: list[dict[str, Any]] = Field(default_factory=list)
    low_performing_products: list[dict[str, Any]] = Field(default_factory=list)
    category_distribution: list[dict[str, Any]] = Field(default_factory=list)
    dead_stock: list[dict[str, Any]] = Field(default_factory=list)
    insights: list[str] = Field(default_factory=list)


class ReportResponse(BaseModel):
    generated_at: str
    row_count: int
    kpis: KPIResponse
    aggregated_data: dict[str, list[dict[str, Any]]] = Field(default_factory=dict)
    dead_stock: list[dict[str, Any]] = Field(default_factory=list)
    low_performing_products: list[dict[str, Any]] = Field(default_factory=list)
