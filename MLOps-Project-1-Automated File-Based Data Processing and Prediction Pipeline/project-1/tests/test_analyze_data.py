# tests/test_analyze_data.py

import unittest
from unittest import mock
import pandas as pd
from scripts.analyze_data import calculate_summary_statistics, sales_by_category, monthly_trends, generate_insights

class TestAnalyzeData(unittest.TestCase):
    def setUp(self):
        # Sample cleaned data
        self.cleaned_data = pd.DataFrame({
            'Date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04'],
            'Store_ID': [101, 102, 103, 101],
            'Product_ID': [1001, 1002, 1003, 1004],
            'Product_Category': ['Electronics', 'Home Appliances', 'Fashion', 'Toys'],
            'Units_Sold': [5, 3, 10, 7],
            'Unit_Price': [299.99, 89.99, 49.99, 19.99],
            'Revenue': [1499.95, 269.97, 499.90, 139.93],
            'Cost': [1200.00, 150.00, 300.00, 150.00],
            'Profit': [299.95, 119.97, 199.90, -10.07]
        })

    def test_calculate_summary_statistics(self):
        summary = calculate_summary_statistics(self.cleaned_data)
        expected_summary = {
            'Total Revenue': 1499.95 + 269.97 + 499.90 + 139.93,  # 2409.75
            'Total Cost': 1200.00 + 150.00 + 300.00 + 150.00,      # 1800.00
            'Total Profit': 299.95 + 119.97 + 199.90 + (-10.07),  # 609.75
            'Average Units Sold': (5 + 3 + 10 + 7) / 4,           # 6.25
            'Average Unit Price': (299.99 + 89.99 + 49.99 + 19.99) / 4  # 114.99
        }
        self.assertAlmostEqual(summary['Total Revenue'], expected_summary['Total Revenue'])
        self.assertAlmostEqual(summary['Total Cost'], expected_summary['Total Cost'])
        self.assertAlmostEqual(summary['Total Profit'], expected_summary['Total Profit'])
        self.assertAlmostEqual(summary['Average Units Sold'], expected_summary['Average Units Sold'])
        self.assertAlmostEqual(summary['Average Unit Price'], expected_summary['Average Unit Price'])

    def test_sales_by_category(self):
        category_summary = sales_by_category(self.cleaned_data)
        expected_summary = pd.DataFrame({
            'Product_Category': ['Electronics', 'Fashion', 'Home Appliances', 'Toys'],
            'Revenue': [1499.95, 499.90, 269.97, 139.93],
            'Profit': [299.95, 199.90, 119.97, -10.07],
            'Units_Sold': [5, 10, 3, 7]
        })
        pd.testing.assert_frame_equal(category_summary.reset_index(drop=True), expected_summary.reset_index(drop=True))

    def test_monthly_trends(self):
        # Mocking pd.to_datetime to ensure dates are parsed correctly
        with mock.patch('scripts.analyze_data.pd.to_datetime', side_effect=lambda x: pd.to_datetime(x)):
            monthly_summary = monthly_trends(self.cleaned_data)
            expected_summary = pd.DataFrame({
                'Month': [pd.Period('2024-01', freq='M')],
                'Revenue': [1499.95 + 269.97 + 499.90 + 139.93],  # 2409.75
                'Profit': [299.95 + 119.97 + 199.90 + (-10.07)]   # 609.75
            })
            self.assertEqual(monthly_summary.shape, expected_summary.shape)
            self.assertAlmostEqual(monthly_summary['Revenue'].iloc[0], expected_summary['Revenue'].iloc[0])
            self.assertAlmostEqual(monthly_summary['Profit'].iloc[0], expected_summary['Profit'].iloc[0])

    @mock.patch('scripts.analyze_data.load_clean_data')
    @mock.patch('scripts.analyze_data.calculate_summary_statistics')
    @mock.patch('scripts.analyze_data.sales_by_category')
    @mock.patch('scripts.analyze_data.monthly_trends')
    def test_generate_insights(self, mock_monthly_trends, mock_sales_by_category, mock_calculate_summary, mock_load_clean_data):
        # Setup mock return values
        mock_df = self.cleaned_data.copy()
        mock_load_clean_data.return_value = mock_df
        mock_calculate_summary.return_value = {'Total Revenue': 2409.75, 'Total Cost': 1800.00, 'Total Profit': 609.75,
                                              'Average Units Sold': 6.25, 'Average Unit Price': 114.99}
        mock_sales_by_category.return_value = pd.DataFrame({
            'Product_Category': ['Electronics', 'Fashion', 'Home Appliances', 'Toys'],
            'Revenue': [1499.95, 499.90, 269.97, 139.93],
            'Profit': [299.95, 199.90, 119.97, -10.07],
            'Units_Sold': [5, 10, 3, 7]
        })
        mock_monthly_trends.return_value = pd.DataFrame({
            'Month': [pd.Period('2024-01', freq='M')],
            'Revenue': [2409.75],
            'Profit': [609.75]
        })

        insights = generate_insights()

        # Assertions
        mock_load_clean_data.assert_called_once()
        mock_calculate_summary.assert_called_once_with(mock_df)
        mock_sales_by_category.assert_called_once_with(mock_df)
        mock_monthly_trends.assert_called_once_with(mock_df)

        expected_insights = {
            'Summary Statistics': {'Total Revenue': 2409.75, 'Total Cost': 1800.00, 'Total Profit': 609.75,
                                    'Average Units Sold': 6.25, 'Average Unit Price': 114.99},
            'Sales by Category': pd.DataFrame({
                'Product_Category': ['Electronics', 'Fashion', 'Home Appliances', 'Toys'],
                'Revenue': [1499.95, 499.90, 269.97, 139.93],
                'Profit': [299.95, 199.90, 119.97, -10.07],
                'Units_Sold': [5, 10, 3, 7]
            }),
            'Monthly Trends': pd.DataFrame({
                'Month': [pd.Period('2024-01', freq='M')],
                'Revenue': [2409.75],
                'Profit': [609.75]
            })
        }

        self.assertEqual(insights['Summary Statistics'], expected_insights['Summary Statistics'])
        pd.testing.assert_frame_equal(insights['Sales by Category'], expected_insights['Sales by Category'])
        pd.testing.assert_frame_equal(insights['Monthly Trends'], expected_insights['Monthly Trends'])

if __name__ == '__main__':
    unittest.main()
