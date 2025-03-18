# generate_report.py

import os
import logging
from analyze_data import generate_insights

# Configure logging
logging.basicConfig(
    filename='generate_report.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

def create_reports_dir(reports_dir='reports/'):
    """
    Ensures that the reports directory exists.
    
    Args:
        reports_dir (str): Path to the reports directory.
    """
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
        logging.info(f"Created reports directory at {reports_dir}")

def format_summary_statistics(summary_stats):
    """
    Formats the summary statistics into a string.
    
    Args:
        summary_stats (dict): Summary statistics.
        
    Returns:
        str: Formatted summary statistics.
    """
    report = "=== Summary Statistics ===\n"
    for key, value in summary_stats.items():
        report += f"{key}: {value}\n"
    report += "\n"
    return report

def format_sales_by_category(category_sales):
    """
    Formats the sales by category into a string.
    
    Args:
        category_sales (pd.DataFrame): Sales by category.
        
    Returns:
        str: Formatted sales by category.
    """
    report = "=== Sales by Category ===\n"
    for index, row in category_sales.iterrows():
        report += (f"Category: {row['Product_Category']}\n"
                   f"  Total Revenue: ${row['Revenue']:.2f}\n"
                   f"  Total Profit: ${row['Profit']:.2f}\n"
                   f"  Units Sold: {row['Units_Sold']}\n\n")
    return report

def format_monthly_trends(monthly_trends):
    """
    Formats the monthly trends into a string.
    
    Args:
        monthly_trends (pd.DataFrame): Monthly revenue and profit trends.
        
    Returns:
        str: Formatted monthly trends.
    """
    report = "=== Monthly Trends ===\n"
    for index, row in monthly_trends.iterrows():
        report += (f"Month: {row['Month']}\n"
                   f"  Total Revenue: ${row['Revenue']:.2f}\n"
                   f"  Total Profit: ${row['Profit']:.2f}\n\n")
    return report

def generate_text_report(insights, report_path='reports/analysis_report.txt'):
    """
    Generates a textual report from the insights and saves it to a file.
    
    Args:
        insights (dict): Insights generated from data analysis.
        report_path (str): Path to save the report.
    """
    try:
        with open(report_path, 'w') as report_file:
            report_file.write("Sales Data Analysis Report\n")
            report_file.write("==========================\n\n")
            
            # Write Summary Statistics
            report_file.write(format_summary_statistics(insights['Summary Statistics']))
            
            # Write Sales by Category
            report_file.write(format_sales_by_category(insights['Sales by Category']))
            
            # Write Monthly Trends
            report_file.write(format_monthly_trends(insights['Monthly Trends']))
        
        logging.info(f"Report generated and saved to {report_path}")
    except Exception as e:
        logging.error(f"Error generating report: {e}")
        raise

def generate_report():
    """
    Orchestrates the report generation process.
    """
    try:
        create_reports_dir()
        insights = generate_insights()
        report_path = os.path.join('reports', 'analysis_report.txt')
        generate_text_report(insights, report_path)
        logging.info("Report generation completed successfully.")
    except Exception as e:
        logging.error(f"Report generation failed: {e}")
        raise

if __name__ == "__main__":
    generate_report()
    print("Report generated successfully. Check the 'reports/' directory for 'analysis_report.txt'.")
