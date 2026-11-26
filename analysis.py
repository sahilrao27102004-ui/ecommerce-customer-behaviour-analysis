from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Run this file from the project folder, or update DATA_FILE if needed.
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "ecommerce_orders_1000.csv"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "python" / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_FILE, parse_dates=["order_date"])

# Basic validation
assert len(df) == 1000, f"Expected 1000 rows, found {len(df)}"
assert df["order_id"].is_unique, "Duplicate order_id values found"
assert df.isna().sum().sum() == 0, "Missing values found"

df["gross_amount"] = df["quantity"] * df["unit_price"]
df["net_amount"] = df["gross_amount"] * (1 - df["discount_pct"] / 100)

delivered = df[df["order_status"] == "Delivered"].copy()

print("ROWS:", len(df))
print("UNIQUE CUSTOMERS:", df["customer_id"].nunique())
print("DELIVERED REVENUE:", round(delivered["net_amount"].sum(), 2))
print("DELIVERED ORDERS:", len(delivered))

category_summary = (
    delivered.groupby("product_category", as_index=False)
    .agg(orders=("order_id", "count"), revenue=("net_amount", "sum"))
    .sort_values("revenue", ascending=False)
)
city_summary = (
    delivered.groupby("city", as_index=False)
    .agg(orders=("order_id", "count"), revenue=("net_amount", "sum"))
    .sort_values("revenue", ascending=False)
)
payment_summary = df.groupby("payment_method", as_index=False).size().rename(columns={"size": "orders"})
monthly_summary = (
    delivered.assign(month=delivered["order_date"].dt.to_period("M").astype(str))
    .groupby("month", as_index=False)["net_amount"].sum()
    .rename(columns={"net_amount": "revenue"})
)

customer_summary = (
    delivered.groupby("customer_id", as_index=False)
    .agg(delivered_orders=("order_id", "count"), customer_revenue=("net_amount", "sum"))
)
customer_summary["customer_type"] = customer_summary["delivered_orders"].apply(
    lambda n: "Repeat" if n > 1 else "One-time"
)

for name, table in {
    "category_summary": category_summary,
    "city_summary": city_summary,
    "payment_summary": payment_summary,
    "monthly_summary": monthly_summary,
    "customer_summary": customer_summary,
}.items():
    table.to_csv(OUTPUT_DIR / f"{name}.csv", index=False)

print("\nCATEGORY SUMMARY\n", category_summary.to_string(index=False))
print("\nCITY SUMMARY\n", city_summary.to_string(index=False))
print("\nCUSTOMER TYPE COUNTS\n", customer_summary["customer_type"].value_counts().to_string())

# Save a clean analysis-ready file for Power BI.
df.to_csv(OUTPUT_DIR / "ecommerce_analysis_ready.csv", index=False)
print(f"\nOutput files saved in: {OUTPUT_DIR}")
