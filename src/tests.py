import unittest
from unittest.mock import MagicMock
from io import StringIO
import csv
import sqlite3
import os
from process_csv.process_csv import process_csv_to_database, process_csv
from db.account_transactions import get_connection, create_database, insert_transactions_to_db


TEST_DB_PATH = 'test_database.db'

class TestDatabaseFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
       
        cls.con = sqlite3.connect(TEST_DB_PATH)

    @classmethod
    def tearDownClass(cls):
        
        cls.con.close()
        os.remove(TEST_DB_PATH)

    def setUp(self):
       
        create_database(self.con)

    def test_insert_transactions(self):
       
        data_to_insert = [(1, '2023-01-15', 45.67, 'Debit'), (2, '2023-01-25', -15.75, 'Credit')]
        insert_transactions_to_db(self.con, data_to_insert)

        
        cursor = self.con.cursor()
        cursor.execute("SELECT * FROM transaction_account")
        rows = cursor.fetchall()

       
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], (1, '2023-01-15', 45.67, 'Debit'))
        self.assertEqual(rows[1], (2, '2023-01-25', -15.75, 'Credit'))

    def test_insert_transactions_error_handling(self):
       
        invalid_data = [(1, '2023-01-15', 45.67, 'Debit'), (2, 'invalid_date', -15.75, 'Credit')]

       
        with self.assertRaises(sqlite3.Error):
            insert_transactions_to_db(self.con, invalid_data)


class TestProcessCSVToDatabase(unittest.TestCase):

    def test_process_csv_to_database(self):

        csv_data = "{'Id':[0,1,2],'Date': [9/15,10/13,11/20],'Transaction':[+45.67,-15.75,+23.2]}"

        csv_file = StringIO(csv_data)


        reader = csv.DictReader(csv_file)


        with unittest.mock.patch('process_csv.process_csv.insert_transactions_to_db') as mock_insert:
            process_csv_to_database(reader)

            expected_data = [
                (unittest.mock.ANY, 45.67, 'Credit'),
                (unittest.mock.ANY, -15.75, 'Debit'),
                (unittest.mock.ANY, 23.2, 'Credit'),
            ]
            mock_insert.assert_called_once_with(expected_data)

class TestProcessCSV(unittest.TestCase):

    def test_process_csv(self):

        reader = {'Id':[0,1,2],'Date': [9/15,10/13,11/20],'Transaction':[+45.67,-15.75,+23.2]}

        result = process_csv(reader)

        expected_result = (
            (100 / 3),  
            (175 / 3),  
            125.0,  
            [
                ["January", 1],
                ["February", 1],
                ["March", 1],
            ],  
        )
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()




