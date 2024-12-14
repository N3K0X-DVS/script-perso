import unittest
import os
import csv
from unittest.mock import patch, mock_open
from lib import equality_check, load_csv, write_csv, sort_data  # Replace with actual module name

class TestFunctions(unittest.TestCase):

    def test_equality_check(self):
        self.assertTrue(equality_check(['a', 'b', 'c'], ['a', 'b', 'c']))
        self.assertFalse(equality_check(['a', 'b', 'c'], ['a', 'b']))
        self.assertFalse(equality_check(['a', 'b', 'c'], ['x', 'y', 'z']))
        self.assertTrue(equality_check([], []))

    @patch("os.listdir", return_value=["test.csv"])
    @patch("builtins.open", new_callable=mock_open, read_data="name,val1,val2,info\ndata1,1.0,2.0,info1\n")
    def test_load_csv_valid_file(self, mock_open_file, mock_listdir):
        header, data = load_csv("test.csv")
        self.assertEqual(header, ["name", "val1", "val2", "info", "département"])
        self.assertEqual(data, [
            ["data1", 1.0, 2.0, "info1", "test"]
        ])
    @patch("os.listdir", return_value=["test.csv"])
    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_load_csv_empty_file(self, mock_open_file, mock_listdir):
        with self.assertRaises(ValueError) as cm:
            load_csv("test.csv")
        self.assertEqual(str(cm.exception), "csv file empty")
    @patch("os.listdir", return_value=["test.csv"])
    @patch("builtins.open", new_callable=mock_open, read_data="name,val1,val2\n")
    def test_load_csv_incorrect_column_count(self, mock_open_file, mock_listdir):
        with self.assertRaises(ValueError) as cm:
            load_csv("test.csv")
        self.assertEqual(str(cm.exception), "csv file must contain exactly 4 columns")
    @patch("os.listdir", return_value=["test.csv"])
    @patch("builtins.open", new_callable=mock_open, read_data="name,val1,val2,info\n")
    def test_load_csv_no_data_rows(self, mock_open_file, mock_listdir):
        with self.assertRaises(ValueError) as cm:
            load_csv("test.csv")
        self.assertEqual(str(cm.exception), "csv file must contain at least 1 header and 1 line of data")
    @patch("os.listdir", return_value=["test.csv"])
    @patch("builtins.open", new_callable=mock_open, read_data="name,val1,val2,info\ndata1,not_a_float,2.0,info1\n")
    def test_load_csv_invalid_data_types(self, mock_open_file, mock_listdir):
        with self.assertRaises(ValueError) as cm:
            load_csv("test.csv")
        self.assertEqual(str(cm.exception), "Row contains invalid data types (expected str, float, float, str)")
    @patch("os.listdir", return_value=[])
    def test_load_csv_file_not_found(self, mock_listdir):
        with self.assertRaises(FileNotFoundError) as cm:
            load_csv("missing.csv")
        self.assertEqual(str(cm.exception), "csv file not in the directory")

    @patch("os.listdir", return_value=["existing.csv"])
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.input", side_effect=['n'])
    def test_write_csv_no_overwrite(self, mock_input, mock_open_file, mock_listdir):
        write_csv("existing.csv", [["data1", 1, 2]], ["col1", "col2", "col3"])
        mock_open_file.assert_not_called()

    @patch("os.listdir", return_value=["existing.csv"])
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.input", side_effect=['yes'])
    def test_write_csv_with_overwrite(self, mock_input, mock_open_file, mock_listdir):
        write_csv("existing.csv", [["data1", 1, 2]], ["col1", "col2", "col3"])
        mock_open_file.assert_called_once_with("existing.csv", "w", newline="", encoding="utf-8")

    def test_sort_data(self):
        header = ["col1", "col2"]
        data = [["data1", 1], ["data2", 2], ["data3", 0]]
        sorted_data = sort_data(data, header, "col2")
        self.assertEqual(sorted_data, [["data3", 0], ["data1", 1], ["data2", 2]])

        sorted_data_desc = sort_data(data, header, "col2", reverse=True)
        self.assertEqual(sorted_data_desc, [["data2", 2], ["data1", 1], ["data3", 0]])

        with self.assertRaises(ValueError):
            sort_data(data, header, "col3")

if __name__ == "__main__":
    unittest.main()