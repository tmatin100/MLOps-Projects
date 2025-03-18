# ingest_data.py

import os
import shutil
import logging

# Configure logging
logging.basicConfig(
    filename='ingest_data.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

def ingest_raw_data(raw_dir='data/raw/', processed_dir='data/processed/'):
    """
    Ingests raw data files from the raw directory and copies them to the processed directory.
    
    Args:
        raw_dir (str): Path to the raw data directory.
        processed_dir (str): Path to the processed data directory.
    """
    try:
        # Ensure processed directory exists
        if not os.path.exists(processed_dir):
            os.makedirs(processed_dir)
            logging.info(f"Created processed data directory at {processed_dir}")
        
        # List all files in the raw directory
        raw_files = [f for f in os.listdir(raw_dir) if f.endswith('.csv') or f.endswith('.json')]
        
        if not raw_files:
            logging.warning(f"No data files found in {raw_dir}.")
            return
        
        for file in raw_files:
            src_path = os.path.join(raw_dir, file)
            dest_path = os.path.join(processed_dir, file)
            
            # Copy file to processed directory
            shutil.copy(src_path, dest_path)
            logging.info(f"Copied {file} to {processed_dir}")
        
        logging.info("Data ingestion completed successfully.")
    
    except Exception as e:
        logging.error(f"Error during data ingestion: {e}")
        raise

if __name__ == "__main__":
    ingest_raw_data()
