import sqlite3

con = sqlite3.connect('transaction_account.db')

cursor = con.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS transaction_account (id INTEGER PRIMARY KEY,date TEXT, money REAL, transaction_type TEXT)''')

def insert_transactions_to_db(data_to_insert):
    cursor.executemany("INSERT INTO transaction_account (date, money, transaction_type) VALUES (?, ?, ?)", data_to_insert)
    con.commit()
    con.close()
