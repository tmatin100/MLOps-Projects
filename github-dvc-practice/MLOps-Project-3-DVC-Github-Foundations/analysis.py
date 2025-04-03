import pandas as pd

def sum_values():
    df = pd.read_csv('data/sample_data.csv')
    return df['value'].sum()

print(f"Sum of values: {sum_values()}")