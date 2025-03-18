# process_data.py

import os
import pandas as pd
import logging

# Configure logging
logging.basicConfig(
    filename='process_data.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

def load_data(processed_dir='data/processed/', filename='sales_data.csv'):
    """
    Loads the sales data CSV file into a pandas DataFrame.
    
    Args:
        processed_dir (str): Path to the processed data directory.
        filename (str): Name of the sales data file.
        
    Returns:
        pd.DataFrame: DataFrame containing the sales data.
    """
    file_path = os.path.join(processed_dir, filename)
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Loaded data from {file_path}")
        return df
    except FileNotFoundError:
        logging.error(f"File {file_path} not found.")
        raise
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        raise

def clean_data(df):
    """
    Cleans the sales data by handling missing values and removing duplicates.
    
    Args:
        df (pd.DataFrame): Raw sales data.
        
    Returns:
        pd.DataFrame: Cleaned sales data.
    """
    try:
        initial_shape = df.shape
        # Handle missing values
        df = df.dropna()
        logging.info(f"Dropped rows with missing values. Shape: {df.shape}")
        
        # Remove duplicates
        df = df.drop_duplicates()
        logging.info(f"Removed duplicates. Shape: {df.shape}")
        
        final_shape = df.shape
        logging.info(f"Data cleaned. Initial shape: {initial_shape}, Final shape: {final_shape}")
        
        return df
    except Exception as e:
        logging.error(f"Error cleaning data: {e}")
        raise

def save_clean_data(df, processed_dir='data/processed/', filename='cleaned_sales_data.csv'):
    """
    Saves the cleaned DataFrame to a CSV file.
    
    Args:
        df (pd.DataFrame): Cleaned sales data.
        processed_dir (str): Path to the processed data directory.
        filename (str): Name of the cleaned data file.
    """
    try:
        file_path = os.path.join(processed_dir, filename)
        df.to_csv(file_path, index=False)
        logging.info(f"Cleaned data saved to {file_path}")
    except Exception as e:
        logging.error(f"Error saving cleaned data: {e}")
        raise

def process_sales_data():
    """
    Orchestrates the data processing steps: loading, cleaning, and saving the data.
    """
    try:
        df = load_data()
        cleaned_df = clean_data(df)
        save_clean_data(cleaned_df)
        logging.info("Data processing completed successfully.")
    except Exception as e:
        logging.error(f"Data processing failed: {e}")
        raise

if __name__ == "__main__":
    process_sales_data()
