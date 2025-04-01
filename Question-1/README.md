# Sales Data Processing

This script processes sales data from two Excel files (`order_region_a.xlsx` and `order_region_b.xlsx`), cleans and transforms the data, and stores it in an SQLite database (`sales.db`). It also validates the data with queries.

## How to Run

1. **Install Dependencies**:
   ```bash
   pip install pandas openpyxl
2. Ensure all required files are in the same directory as sales_process.py.
3. RUN the Script:
    python sales_process.py

## Features
- Combines data from two regions (A and B).
- Removes duplicate OrderId records.
- Extracts PromotionDiscount from JSON strings.
- Calculates total_sales and net_sale (removes negative/zero sales).
- Stores processed data in sales.db (table: sales_data).
- Runs validation queries (e.g., total records, sales by region, duplicates).

## Assumptions
- Input files have columns: OrderId, QuantityOrdered, ItemPrice, PromotionDiscount.
- Invalid PromotionDiscount JSON defaults to 0.
- Negative or zero net_sale records are excluded.

## Output
Processed data is saved in sales.db.
Validation results are printed to the console.