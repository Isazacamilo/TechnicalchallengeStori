import sqlite3
from config import DB_URL

def get_connection():
    con = sqlite3.connect(DB_URL)
    return con

def create_database():
    cursor = get_connection().cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS transaction_account (id INTEGER PRIMARY KEY,date TEXT, money REAL, transaction_type TEXT)''')


def insert_transactions_to_db(data_to_insert):
    create_database()
    cursor = get_connection().cursor()
    cursor.executemany("INSERT INTO transaction_account (date, money, transaction_type) VALUES (?, ?, ?)", data_to_insert)
    get_connection().commit()
    get_connection().close()
    print("Successfully inserted records in database")
