import requests
import csv
from io import StringIO
from process_csv.process_csv import process_csv, process_csv_to_database



def read_local_file(file):
    with open(file, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
        transactions_details = process_csv(data)
        process_csv_to_database(data)
    return transactions_details


def read_s3_bucket(file):
    s3_bucket_url = 'https://s3.amazonaws.com/your-bucket-name'
    file_key = 'path/to/your/file.csv'

    try:
        s3_file_url = f'{s3_bucket_url}/{file_key}'
        response = requests.get(s3_file_url)

        if response.status_code == 200:
            csv_content = response.text
        else:
            print(f"Failed to fetch the file from S3. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error fetching the file from S3: {str(e)}")
        csv_content = None


    if csv_content is not None:
        with StringIO(csv_content) as csvfile:
            reader = csv.DictReader(csvfile)
    return reader


def file_location(file):
    if file.startswith("s3://"):
        return read_s3_bucket(file)

    else:
        return read_local_file(file)
