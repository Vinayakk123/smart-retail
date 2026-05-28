
import pandas as pd
import random
from datetime import datetime, timedelta

products = [
    ("Rice", "Grains", 40, 55),
    ("Milk", "Dairy", 25, 35),
    ("Bread", "Bakery", 20, 30),
    ("Biscuits", "Snacks", 10, 20),
    ("Chips", "Snacks", 15, 30),
    ("Coffee", "Beverages", 100, 150),
    ("Tea Powder", "Beverages", 80, 120),
    ("Soap", "Personal Care", 20, 35),
    ("Shampoo", "Personal Care", 70, 110),
    ("Oil", "Groceries", 90, 130),
]

data = []

start_date = datetime(2026, 1, 1)

for i in range(300):
    product = random.choice(products)
    date = start_date + timedelta(days=random.randint(0, 90))
    
    quantity = random.randint(5, 60)

    data.append([
        date.strftime("%Y-%m-%d"),
        product[0],
        product[1],
        product[2],
        product[3],
        quantity
    ])

df = pd.DataFrame(data, columns=[
    "Date", "Product Name", "Category",
    "Cost Price", "Selling Price", "Quantity"
])

df.to_csv("smart_retail_data.csv", index=False)