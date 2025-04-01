import pandas as pd
import sqlite3
import json

df_a = pd.read_excel("order_region_a.xlsx")
df_b = pd.read_excel("order_region_b.xlsx")


# Add region column
df_a["region"] = "A"
df_b["region"] = "B"

# Combine data
df = pd.concat([df_a, df_b])

# Remove duplicate OrderId records
df = df.drop_duplicates(subset=["OrderId"])

def extract_discount_amount(promo_json):
    """
    Extracts the discount amount from the PromotionDiscount(JSON string)
    Args:
        promo_json (str): JSON string containing the discount information.
    Returns:
        float: The discount amount extracted from the JSON string.        
    """
    try:
        promo_dict = json.loads(promo_json)
        return float(promo_dict.get("Amount", 0))
    except Exception as ex:
        print(f"Error processing PromotionDiscount: {promo_json} -> {ex}")
        return 0
df["PromotionDiscount"] = df["PromotionDiscount"].astype(str).apply(extract_discount_amount)

# Calculate total_sales and net_sales
df["total_sales"] = df["QuantityOrdered"] * df["ItemPrice"]
df["net_sale"] = df["total_sales"] - df["PromotionDiscount"]

# # Remove negative or zero net sales
df = df[df["net_sale"] > 0]

# Load into SQLite database
conn = sqlite3.connect("sales.db")
df.to_sql("sales_data", conn, if_exists="replace", index=False)

# Validation Queries
def validate_data():
    queries = {
        "Total Records": """
            SELECT COUNT(*) AS total_records 
            FROM sales_data;
        """,
        
        "Total Sales by Region": """
            SELECT 
                region, 
                SUM(net_sale) AS total_sales 
            FROM sales_data 
            GROUP BY region;
        """,
        
        "Average Sales per Transaction": """
            SELECT 
                AVG(net_sale) AS avg_sales_per_transaction 
            FROM sales_data;
        """,
        
        "Duplicate Order Check": """
            SELECT 
                OrderId, 
                COUNT(*) AS duplicate_count 
            FROM sales_data 
            GROUP BY OrderId 
            HAVING COUNT(*) > 1;
        """
    }

    for desc, query in queries.items():        
        result = conn.execute(query).fetchall()
        if result:
            print(f'{desc}:{result[0][0]}')
        else:
            print(f'{desc}: No data found')
validate_data()
conn.close()
