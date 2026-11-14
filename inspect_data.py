from pathlib import Path
import pandas as pd

raw = Path(__file__).resolve().parent / 'data' / 'raw'
orders = pd.read_csv(raw / 'olist_orders_dataset.csv')
customers = pd.read_csv(raw / 'olist_customers_dataset.csv')
print('Orders shape:', orders.shape)
print('Customers shape:', customers.shape)
print(orders.head(3).to_string())
print(orders.dtypes)
print(orders.isna().sum())
print(orders['order_status'].value_counts(dropna=False))
print('Duplicate order IDs:', orders['order_id'].duplicated().sum())
print('Duplicate customer IDs:', customers['customer_id'].duplicated().sum())
