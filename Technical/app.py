from process_csv.process_csv import process_csv, process_csv_to_database
from mail.send_notification import send_notification

def main():
    transaction_account = 'Transactions/account.csv'
    transactions_details = process_csv(transaction_account)
    process_csv_to_database(transaction_account)
    send_notification(*transactions_details)

if __name__ == '__main__':
    main()