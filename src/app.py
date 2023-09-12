from mail.send_notification import send_notification
from config import FILE
from context import get_file_reader
from process_csv.process_csv import process_csv_to_database
import json



def lambda_handler(event, context):
    transaction_account = FILE
    print("Getting file reader")
    file_reader = get_file_reader(transaction_account)
    print("Reading file")
    transactions_details = file_reader(transaction_account)
    print("Inserting records in database")
    process_csv_to_database(transactions_details)
    print("Sending notification")
    send_notification(*transactions_details)
    
    return {
        'statusCode': 200,
    }
    


def main():
    transaction_account = FILE
    print("Getting file reader")
    file_reader = get_file_reader(transaction_account)
    print("Reading file")
    transactions_details = file_reader(transaction_account)
    print("Inserting records in database")
    process_csv_to_database(transactions_details)
    print("Sending notification")
    send_notification(*transactions_details)
    

if __name__ == '__main__':
    main()