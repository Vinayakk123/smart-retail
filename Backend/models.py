from dataclasses import dataclass

TABLE_NAME = "retail_transactions"

DB_COLUMNS = [
    "date",
    "product_name",
    "category",
    "cost_price",
    "selling_price",
    "quantity",
    "revenue",
    "profit",
    "profit_margin",
]


@dataclass(slots=True)
class RetailRecord:
    date: str
    product_name: str
    category: str
    cost_price: float
    selling_price: float
    quantity: float
    revenue: float
    profit: float
    profit_margin: float
