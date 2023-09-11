import unittest
from unittest.mock import MagicMock
from io import StringIO
import csv
from process_csv.process_csv import process_csv_to_database, process_csv

class TestProcessCSVToDatabase(unittest.TestCase):

    def test_process_csv_to_database(self):
        # Sample CSV data as a string
        csv_data = """id,date,Transaction
        0,9/15,+45.67
        1,10/13,-15.75
        2,11/20,+23.2"""

        # Convert the CSV data string into a StringIO object
        csv_file = StringIO(csv_data)

        # Create a DictReader to read the data
        reader = csv.DictReader(csv_file)

        # Mock insert_transactions_to_db function
        with unittest.mock.patch('process_csv.process_csv.insert_transactions_to_db') as mock_insert:
            process_csv_to_database(reader)

            # Assert that insert_transactions_to_db was called with the correct data
            expected_data = [
                (unittest.mock.ANY, 45.67, 'Credit'),
                (unittest.mock.ANY, -15.75, 'Debit'),
                (unittest.mock.ANY, 23.2, 'Credit'),
            ]
            mock_insert.assert_called_once_with(expected_data)

class TestProcessCSV(unittest.TestCase):

    def test_process_csv(self):
        # Mock the reader
        reader = [
            {"date": "01/01", "Transaction": "100"},
            {"date": "02/01", "Transaction": "-50"},
            {"date": "03/01", "Transaction": "75"},
        ]

        # Call the function and capture the results
        result = process_csv(reader)

        # Assert the expected results
        expected_result = (
            (100 / 3),  # Average Debit
            (175 / 3),  # Average Credit
            125.0,  # Total Balance
            [
                ["January", 1],
                ["February", 1],
                ["March", 1],
            ],  # Year-Month with Transactions
        )
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
