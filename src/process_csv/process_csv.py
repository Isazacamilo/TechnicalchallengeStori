import csv
from datetime import datetime
from enum import Enum
from db.account_transactions import insert_transactions_to_db
from config import DB_URL


def process_csv_to_database(reader):
    if DB_URL:
        data_to_insert = []
        
        for row in reader:
            date = datetime.strptime(row["Date"], "%m/%d").replace(year=2023)
            transaction_value = float(row["Transaction"])
            data_to_insert.append((date, transaction_value, process_transaction_type(transaction_value)))
        print("Inserting records in database")
        insert_transactions_to_db(data_to_insert)        


def process_transaction_type(transaction):
    class TransactionType(Enum):
        CREDITS = "Credit"
        DEBIT = "Debit"

    return (TransactionType.DEBIT).value if transaction < 0 else (TransactionType.CREDITS).value


def process_csv(reader):
    total_balance = 0
    total_debit = 0
    total_credit = 0

    year = {
        1: ["January", 0],
        2: ["February", 0],
        3: ["March", 0],
        4: ["April", 0],
        5: ["May", 0],
        6: ["June", 0],
        7: ["July", 0],
        8: ["August", 0],
        9: ["September", 0],
        10: ["October", 0],
        11: ["November", 0],
        12: ["December", 0],
    }

    for row in reader:
        date = datetime.strptime(row["Date"], "%m/%d")
        transaction = float(row["Transaction"])

        total_balance += transaction

        year[date.month][1] += 1

        if transaction < 0:
            total_debit += transaction
        else:
            total_credit += transaction

    year_month_with_transactions = {
        month: transaction_data
        for month, transaction_data in year.items()
        if transaction_data[1] > 0
        }
    year_month_with_transactions = list(year_month_with_transactions.values())

    average_debit = total_debit / (len(year_month_with_transactions))
    average_credit = total_credit / (len(year_month_with_transactions))

    return average_debit, average_credit, total_balance, year_month_with_transactions
