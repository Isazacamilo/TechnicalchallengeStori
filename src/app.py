from mail.send_notification import send_notification
from config import FILE
from context import get_file_reader

def main():
    transaction_account = FILE
    print("Getting file reader")
    file_reader = get_file_reader(transaction_account)
    print("Reading file")
    transactions_details = file_reader(transaction_account)
    print("Sending notification")
    send_notification(*transactions_details)

if __name__ == '__main__':
    main()