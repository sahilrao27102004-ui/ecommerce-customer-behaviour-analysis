# Project 02 — E-Commerce Customer Behaviour Analysis

## Files
- `data/ecommerce_orders_1000.csv` — exactly 1,000 synthetic order records.
- `sql/01_create_and_load_database.sql` — creates the database/table and loads all rows using SQL INSERT statements. This avoids the MySQL Workbench Import Wizard.
- `sql/02_analysis_queries.sql` — starter analysis queries.
- `python/analysis.py` — Pandas analysis and CSV exports for Power BI.

## Step 1 — Extract
Extract the ZIP file. Keep the folder structure unchanged.

## Step 2 — Load data into MySQL Workbench (no CSV Import Wizard)
1. Open MySQL Workbench and connect to your local MySQL connection.
2. Select **File > Open SQL Script**.
3. Open `sql/01_create_and_load_database.sql`.
4. Click the lightning-bolt Execute button.
5. Wait for execution to finish. The script creates `ecommerce_customer_analysis`, creates one table, and inserts 1,000 rows.
6. Run:
   `USE ecommerce_customer_analysis;`
   `SELECT COUNT(*) FROM ecommerce_orders;`
7. Expected count: **1000**.

Important: This setup script intentionally drops and recreates only the `ecommerce_orders` table in this new project database. Do not run it in a database containing data you need to keep.

## Step 3 — Run SQL analysis
Open `sql/02_analysis_queries.sql` and execute queries one by one. The script begins with `USE ecommerce_customer_analysis;`.

## Step 4 — Run Python analysis
1. Install Python if required.
2. Open VS Code and open the extracted project folder.
3. Open Terminal > New Terminal.
4. Install packages:
   `python -m pip install pandas matplotlib`
5. Run:
   `python python/analysis.py`
6. The script checks the row count, duplicate order IDs and missing values, then creates output CSVs in `python/outputs/`.

If `python` is not recognized on Windows, try `py -m pip install pandas matplotlib` and `py python/analysis.py`.

## Step 5 — Power BI
1. Open Power BI Desktop.
2. Choose **Get data > Text/CSV**.
3. Select `python/outputs/ecommerce_analysis_ready.csv`.
4. Click **Load**.
5. Create visuals:
   - Cards: delivered revenue, total orders, unique customers.
   - Bar chart: revenue by product category.
   - Bar chart: revenue by city.
   - Donut chart: orders by payment method.
   - Line chart: monthly revenue.
   - Donut/bar chart: one-time vs repeat customers.

For revenue in Power BI, use the `net_amount` column and filter `order_status` to `Delivered`.

## Dataset notes
This is a practice dataset generated for this portfolio project, not real customer or company data. Revenue is calculated as quantity × unit price after discount. Cancelled and returned orders are excluded from delivered revenue.
