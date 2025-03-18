# tests/test_process_data.py

import unittest
from unittest import mock
import pandas as pd
from io import StringIO
from scripts.process_data import load_data, clean_data, save_clean_data

class TestProcessData(unittest.TestCase):
    @mock.patch('scripts.process_data.pd.read_csv')
    @mock.patch('scripts.process_data.os.path')
    def test_load_data_success(self, mock_path, mock_read_csv):
        mock_path.join.return_value = 'data/processed/sales_data.csv'
        mock_read_csv.return_value = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})

        df = load_data(processed_dir='data/processed/', filename='sales_data.csv')

        mock_read_csv.assert_called_once_with('data/processed/sales_data.csv')
        self.assertEqual(df.shape, (2, 2))

    @mock.patch('scripts.process_data.pd.read_csv')
    @mock.patch('scripts.process_data.os.path')
    def test_load_data_file_not_found(self, mock_path, mock_read_csv):
        mock_path.join.return_value = 'data/processed/sales_data.csv'
        mock_read_csv.side_effect = FileNotFoundError

        with self.assertRaises(FileNotFoundError):
            load_data(processed_dir='data/processed/', filename='sales_data.csv')

    def test_clean_data_success(self):
        raw_data = {
            'A': [1, 2, None, 4],
            'B': [5, None, 7, 8],
            'C': [9, 10, 11, 12]
        }
        df = pd.DataFrame(raw_data)
        cleaned_df = clean_data(df)

        # After dropping rows with any NaN, only rows with all values present remain
        expected_df = pd.DataFrame({
            'A': [1, 4],
            'B': [5, 8],
            'C': [9, 12]
        })
        pd.testing.assert_frame_equal(cleaned_df.reset_index(drop=True), expected_df.reset_index(drop=True))

    def test_clean_data_remove_duplicates(self):
        raw_data = {
            'A': [1, 1, 2, 3],
            'B': [5, 5, 7, 8],
            'C': [9, 9, 11, 12]
        }
        df = pd.DataFrame(raw_data)
        cleaned_df = clean_data(df)

        # After removing duplicates, one duplicate row should be removed
        expected_df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [5, 7, 8],
            'C': [9, 11, 12]
        })
        pd.testing.assert_frame_equal(cleaned_df.reset_index(drop=True), expected_df.reset_index(drop=True))

    @mock.patch('scripts.process_data.pd.DataFrame.to_csv')
    @mock.patch('scripts.process_data.os.path')
    def test_save_clean_data_success(self, mock_path, mock_to_csv):
        df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        mock_path.join.return_value = 'data/processed/cleaned_sales_data.csv'

        save_clean_data(df, processed_dir='data/processed/', filename='cleaned_sales_data.csv')

        df.to_csv.assert_called_once_with('data/processed/cleaned_sales_data.csv', index=False)

    @mock.patch('scripts.process_data.pd.DataFrame.to_csv')
    @mock.patch('scripts.process_data.os.path')
    def test_save_clean_data_exception(self, mock_path, mock_to_csv):
        df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        mock_path.join.return_value = 'data/processed/cleaned_sales_data.csv'
        mock_to_csv.side_effect = Exception("Save failed")

        with self.assertRaises(Exception):
            save_clean_data(df, processed_dir='data/processed/', filename='cleaned_sales_data.csv')

if __name__ == '__main__':
    unittest.main()
