import os
import unittest
import tempfile
import csv
import shutil

# Import the functions to be tested
from lib import (
    equality_check,
    load_csv,
    write_csv,
    sort_data
)


class TestCSVUtilityFunctions(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the temporary directory after tests
        shutil.rmtree(self.test_dir)

    def test_equality_check(self):
        # Test equal arrays
        self.assertTrue(equality_check(['a', 'b', 'c'], ['a', 'b', 'c']))

        # Test unequal arrays (different length)
        self.assertFalse(equality_check(['a', 'b'], ['a', 'b', 'c']))

        # Test unequal arrays (same length, different content)
        self.assertFalse(equality_check(['a', 'b', 'c'], ['a', 'b', 'd']))

        # Test empty arrays
        self.assertTrue(equality_check([], []))

    def test_load_csv_success(self):
        # Create a test CSV file
        test_file_path = os.path.join(self.test_dir, 'test_data.csv')
        with open(test_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows([
                ['Name', 'Value1', 'Value2', 'Category'],
                ['Item1', '10.5', '20.3', 'A'],
                ['Item2', '15.7', '25.6', 'B']
            ])

        # Test successful CSV loading
        header, data = load_csv('test_data.csv', self.test_dir)

        # Check header
        expected_header = ['Name', 'Value1', 'Value2', 'Category', 'département']
        self.assertEqual(header, expected_header)

        # Check data
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0][0], 'Item1')
        self.assertEqual(float(data[0][1]), 10.5)
        self.assertEqual(float(data[0][2]), 20.3)
        self.assertEqual(data[0][3], 'A')
        self.assertEqual(data[0][4], 'test_data')

    def test_load_csv_error_cases(self):
        # Test file not found
        with self.assertRaises(FileNotFoundError):
            load_csv('nonexistent.csv', self.test_dir)

        # Test empty file
        test_file_path = os.path.join(self.test_dir, 'empty.csv')
        open(test_file_path, 'w').close()
        with self.assertRaises(ValueError):
            load_csv('empty.csv', self.test_dir)

        # Test insufficient columns
        test_file_path = os.path.join(self.test_dir, 'insufficient_cols.csv')
        with open(test_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows([
                ['Name', 'Value'],
                ['Item1', '10']
            ])
        with self.assertRaises(ValueError):
            load_csv('insufficient_cols.csv', self.test_dir)

        # Test invalid data types
        test_file_path = os.path.join(self.test_dir, 'invalid_types.csv')
        with open(test_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows([
                ['Name', 'Value1', 'Value2', 'Category'],
                ['Item1', 'not_a_number', '20.3', 'A']
            ])
        with self.assertRaises(ValueError):
            load_csv('invalid_types.csv', self.test_dir)

    def test_write_csv(self):
        # Prepare test data
        header = ['Name', 'Value1', 'Value2', 'Category', 'département']
        data = [
            ['Item1', '10.5', '20.3', 'A', 'test_dept'],
            ['Item2', '15.7', '25.6', 'B', 'test_dept']
        ]
        output_file = 'output_test.csv'
        output_path = os.path.join(self.test_dir, output_file)

        # Test writing CSV
        write_csv(output_file, data, header, self.test_dir, force_overwrite=True)

        # Verify file was created and contents are correct
        self.assertTrue(os.path.exists(output_path))

        with open(output_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            read_rows = list(reader)

        self.assertEqual(read_rows[0], header)
        self.assertEqual(read_rows[1], ['Item1', '10.5', '20.3', 'A', 'test_dept'])
        self.assertEqual(read_rows[2], ['Item2', '15.7', '25.6', 'B', 'test_dept'])

    def test_sort_data(self):
        # Prepare test data
        header = ['Name', 'Value', 'Category']
        data = [
            ['Item1', 10, 'B'],
            ['Item2', 5, 'A'],
            ['Item3', 15, 'C']
        ]

        # Test sorting by Name (ascending)
        sorted_data = sort_data(data, header, 'Name')
        self.assertEqual([row[0] for row in sorted_data], ['Item1', 'Item2', 'Item3'])

        # Test sorting by Name (descending)
        sorted_data = sort_data(data, header, 'Name', reverse=True)
        self.assertEqual([row[0] for row in sorted_data], ['Item3', 'Item2', 'Item1'])

        # Test sorting by Value (ascending)
        sorted_data = sort_data(data, header, 'Value')
        self.assertEqual([row[0] for row in sorted_data], ['Item2', 'Item1', 'Item3'])

        # Test invalid column raises ValueError
        with self.assertRaises(ValueError):
            sort_data(data, header, 'InvalidColumn')


if __name__ == '__main__':
    unittest.main()