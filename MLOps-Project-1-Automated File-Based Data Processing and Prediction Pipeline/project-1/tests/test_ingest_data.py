# tests/test_ingest_data.py

import unittest
from unittest import mock
import os
import shutil
from scripts.ingest_data import ingest_raw_data

class TestIngestData(unittest.TestCase):
    @mock.patch('scripts.ingest_data.os')
    @mock.patch('scripts.ingest_data.shutil')
    def test_ingest_raw_data_success(self, mock_shutil, mock_os):
        # Setup mock for os.path.exists
        mock_os.path.exists.return_value = False  # Simulate that processed_dir does not exist

        # Setup mock for os.listdir
        mock_os.listdir.return_value = ['sales_data.csv', 'extra_data.json']

        # Call the function
        ingest_raw_data(raw_dir='data/raw/', processed_dir='data/processed/')

        # Assertions
        mock_os.makedirs.assert_called_once_with('data/processed/')
        self.assertEqual(mock_shutil.copy.call_count, 2)
        mock_shutil.copy.assert_any_call('data/raw/sales_data.csv', 'data/processed/sales_data.csv')
        mock_shutil.copy.assert_any_call('data/raw/extra_data.json', 'data/processed/extra_data.json')

    @mock.patch('scripts.ingest_data.os')
    @mock.patch('scripts.ingest_data.shutil')
    def test_ingest_raw_data_no_files(self, mock_shutil, mock_os):
        # Setup mock for os.path.exists
        mock_os.path.exists.return_value = True  # processed_dir exists

        # Setup mock for os.listdir to return empty list
        mock_os.listdir.return_value = []

        # Call the function
        ingest_raw_data(raw_dir='data/raw/', processed_dir='data/processed/')

        # Assertions
        mock_os.makedirs.assert_not_called()
        mock_shutil.copy.assert_not_called()

    @mock.patch('scripts.ingest_data.os')
    @mock.patch('scripts.ingest_data.shutil')
    def test_ingest_raw_data_exception(self, mock_shutil, mock_os):
        # Setup mock to raise an exception when copying
        mock_os.path.exists.return_value = True
        mock_os.listdir.return_value = ['sales_data.csv']
        mock_shutil.copy.side_effect = Exception("Copy failed")

        # Expect the function to raise an exception
        with self.assertRaises(Exception) as context:
            ingest_raw_data(raw_dir='data/raw/', processed_dir='data/processed/')

        self.assertTrue("Copy failed" in str(context.exception))

if __name__ == '__main__':
    unittest.main()
