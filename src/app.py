from mail.send_notification import send_notification
from config import FILE
from context import file_location, read_local_file

def main():
    transaction_account = FILE
    transactions_details = file_location(transaction_account)
    send_notification(*transactions_details)

if __name__ == '__main__':
    main()