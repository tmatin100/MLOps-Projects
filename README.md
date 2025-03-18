# MLOps-Projects

# MLOps Project 1 : Automated File-Based Data Processing and Prediction Pipeline

## **Primary Goal**
Develop an end-to-end pipeline that automates the ingestion, processing, analysis, and reporting of sales data.

- **Ingestion**
- **Processing**
- **Analysis**
- **Reporting**

## **Project Scope**
- Utilize Python scripts to manage data workflows.
- Generate reports to summarize data insights.

## **Project File Structure**




## **1. Data Ingestion**
- **Script**: `ingest_data.py`
- **Purpose**:
    - Ingest raw sales data from `data/raw/` and copy it to the `data/processed/` folder.
- **Key Function**:
    - `ingest_raw_data`: Handles copying of files.

## **2. Data Processing**
- **Script**: `process_data.py`
- **Purpose**:
    - Cleans and preprocesses the ingested sales data.
- **Key Functions**:
    - `load_data`: Loads raw data into a DataFrame.
    - `clean_data`: Handles missing values and removes duplicates.
    - `save_clean_data`: Saves the cleaned data.
- **Workflow**:
    - Load raw data.
    - Clean data by removing incomplete and duplicate records.
    - Save cleaned data for analysis.

## **3. Data Analysis**
- **Script**: `analyze_data.py`
- **Purpose**:
    - Perform analysis on the cleaned sales data to generate insights.
- **Key Functions**:
    - `calculate_summary_statistics`: Compute totals and averages.
    - `sales_by_category`: Aggregates sales by product category.
    - `monthly_trends`: Analyzes revenue and trends over months.
    - `generate_insights`: Orchestrates the analysis process.
- **Workflow**:
    - Load cleaned data.
    - Perform various statistical analyses.
    - Compile insights for reporting.

## **4. Generate Report**
- **Script**: `generate_report.py`
- **Purpose**:
    - Generate a comprehensive textual report summarizing the analysis.
- **Key Functions**:
    - `create_reports_dir`: Ensures the `reports/` directory exists.
    - `format_summary_statistics`: Formats summary statistics.
    - `format_sales_by_category`: Formats sales by category.
    - `format_monthly_trends`: Formats monthly trends.
    - `generate_text_report`: Compiles and saves the report to a text file.
- **Workflow**:
    - Fetch insights from `analyze_data.py`.
    - Format the insights into readable sections.
    - Save the report to the `reports/` directory.

## **Script Execution Order**
Run the scripts in the following order:
```sh
python scripts/ingest_data.py
python scripts/process_data.py
python scripts/analyze_data.py
python scripts/generate_report.py

