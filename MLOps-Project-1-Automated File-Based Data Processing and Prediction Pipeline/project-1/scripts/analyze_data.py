# analyze_data.py

import os
import pandas as pd
import logging

# Configure logging
logging.basicConfig(
    filename='analyze_data.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

def load_clean_data(processed_dir='data/processed/', filename='cleaned_sales_data.csv'):
    """
    Loads the cleaned sales data into a pandas DataFrame.
    
    Args:
        processed_dir (str): Path to the processed data directory.
        filename (str): Name of the cleaned sales data file.
        
    Returns:
        pd.DataFrame: Cleaned sales data.
    """
    file_path = os.path.join(processed_dir, filename)
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Loaded cleaned data from {file_path}")
        return df
    except FileNotFoundError:
        logging.error(f"File {file_path} not found.")
        raise
    except Exception as e:
        logging.error(f"Error loading cleaned data: {e}")
        raise

def calculate_summary_statistics(df):
    """
    Calculates summary statistics for numerical columns.
    
    Args:
        df (pd.DataFrame): Cleaned sales data.
        
    Returns:
        dict: Summary statistics.
    """
    try:
        summary = {
            'Total Revenue': df['Revenue'].sum(),
            'Total Cost': df['Cost'].sum(),
            'Total Profit': df['Profit'].sum(),
            'Average Units Sold': df['Units_Sold'].mean(),
            'Average Unit Price': df['Unit_Price'].mean()
        }
        logging.info("Calculated summary statistics.")
        return summary
    except Exception as e:
        logging.error(f"Error calculating summary statistics: {e}")
        raise

def sales_by_category(df):
    """
    Calculates total sales and profit by product category.
    
    Args:
        df (pd.DataFrame): Cleaned sales data.
        
    Returns:
        pd.DataFrame: Sales and profit by category.
    """
    try:
        category_summary = df.groupby('Product_Category').agg({
            'Revenue': 'sum',
            'Profit': 'sum',
            'Units_Sold': 'sum'
        }).reset_index()
        logging.info("Calculated sales by category.")
        return category_summary
    except Exception as e:
        logging.error(f"Error calculating sales by category: {e}")
        raise

def monthly_trends(df):
    """
    Analyzes monthly trends in revenue and profit.
    
    Args:
        df (pd.DataFrame): Cleaned sales data.
        
    Returns:
        pd.DataFrame: Monthly revenue and profit trends.
    """
    try:
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.to_period('M')
        monthly_summary = df.groupby('Month').agg({
            'Revenue': 'sum',
            'Profit': 'sum'
        }).reset_index()
        logging.info("Analyzed monthly trends.")
        return monthly_summary
    except Exception as e:
        logging.error(f"Error analyzing monthly trends: {e}")
        raise

def generate_insights():
    """
    Generates insights by performing various analyses on the sales data.
    
    Returns:
        dict: Contains summary statistics, sales by category, and monthly trends.
    """
    try:
        df = load_clean_data()
        summary_stats = calculate_summary_statistics(df)
        category_sales = sales_by_category(df)
        trends = monthly_trends(df)
        
        insights = {
            'Summary Statistics': summary_stats,
            'Sales by Category': category_sales,
            'Monthly Trends': trends
        }
        logging.info("Generated all insights.")
        return insights
    except Exception as e:
        logging.error(f"Error generating insights: {e}")
        raise

if __name__ == "__main__":
    insights = generate_insights()
    # For demonstration purposes, print the insights
    print("Summary Statistics:")
    for key, value in insights['Summary Statistics'].items():
        print(f"{key}: {value}")
    
    print("\nSales by Category:")
    print(insights['Sales by Category'])
    
    print("\nMonthly Trends:")
    print(insights['Monthly Trends'])
