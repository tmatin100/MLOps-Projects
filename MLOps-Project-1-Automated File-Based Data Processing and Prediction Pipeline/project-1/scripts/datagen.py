import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Parameters
num_days = 30
start_date = datetime(2024, 1, 1)
store_ids = [101, 102, 103]
product_ids = {
    1001: 'Electronics',
    1002: 'Home Appliances',
    1003: 'Fashion',
    1004: 'Toys',
    1005: 'Books',
    1006: 'Groceries',
    1007: 'Beauty',
    1008: 'Sports',
    1009: 'Automotive',
    1010: 'Health',
    1011: 'Stationery',
    1012: 'Garden'
}

data = []

np.random.seed(42)  # For reproducibility

for day in range(num_days):
    current_date = start_date + timedelta(days=day)
    for store in store_ids:
        # Random number of transactions per store per day
        num_transactions = np.random.randint(1, 5)
        for _ in range(num_transactions):
            product_id = np.random.choice(list(product_ids.keys()))
            category = product_ids[product_id]
            units_sold = np.random.randint(1, 100)
            unit_price = round(np.random.uniform(1.0, 500.0), 2)
            revenue = round(units_sold * unit_price, 2)
            cost = round(revenue * np.random.uniform(0.5, 0.9), 2)
            profit = round(revenue - cost, 2)
            
            data.append([
                current_date.strftime('%Y-%m-%d'),
                store,
                product_id,
                category,
                units_sold,
                unit_price,
                revenue,
                cost,
                profit
            ])

# Create DataFrame
columns = ['Date', 'Store_ID', 'Product_ID', 'Product_Category', 'Units_Sold',
           'Unit_Price', 'Revenue', 'Cost', 'Profit']

df = pd.DataFrame(data, columns=columns)

# Save to CSV
df.to_csv('sales_data.csv', index=False)

print("Dummy sales_data.csv generated successfully!")
