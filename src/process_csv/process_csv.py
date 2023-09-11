import csv
from datetime import datetime
from enum import Enum
from db.account_transactions import insert_transactions_to_db


def process_csv_to_database(reader):
    data_to_insert = []

    # with open(transaction_account, "r") as csvfile:
    #     reader = csv.DictReader(csvfile)
    for row in reader:
        date = datetime.strptime(row["date"], "%m/%d").replace(year=2023)
        transaction_value = float(row["Transaction"])
        data_to_insert.append(
            (date, transaction_value, process_transaction_type(transaction_value))
        )
    insert_transactions_to_db(data_to_insert)


def process_transaction_type(transaction):
    class TransactionType(Enum):
        CREDITS = "Credit"
        DEBIT = "Debit"

    return (TransactionType.CREDITS).value if transaction < 0 else (TransactionType.DEBIT).value


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
    # with open(transaction_account, "r") as csvfile:
    #     reader = csv.DictReader(csvfile)

    for row in reader:
        date = datetime.strptime(row["date"], "%m/%d")
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
