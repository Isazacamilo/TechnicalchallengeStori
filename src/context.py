import requests
import csv
from io import StringIO
from process_csv.process_csv import process_csv, process_csv_to_database



def read_local_file(file):
    with open(file, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
        process_csv_to_database(data)
        return process_csv(data)


def read_s3_bucket(file):

    try:
        s3_file_url = f'{file}'
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
            data = list(reader)
            process_csv_to_database(data)
            return  process_csv(data)


def get_file_reader(file):
    if file.startswith("https://"):
        return read_s3_bucket
    else:
        return read_local_file
