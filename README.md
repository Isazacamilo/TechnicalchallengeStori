# Account CSV Reader

The Account CSV Reader is a project designed to read an account CSV file and send an email to the user containing their account balance and a summary of the number of transactions for each month.


## Configuration
To run the project locally, you need to configure a .env file with the following variables:
- FILE: The path to the CSV file containing account data (e.g., "transactions/account.csv").
- LOGO: The path to the logo file you want to include in the email (e.g., "./logo/stori.png").
- PASSWORD: The SMTP password for the email account used to send emails.
- SMTP_USERNAME: The SMTP username or email address for the email account.
- FROM: The email address from which the email will be sent.
- TO: The recipient's email address.

Make sure to replace these example values with your actual configuration.

## How to Run

To build the Docker image, use the following command, replacing <name that you want> with your desired image name:

`docker build -t <name that you want> .`

To run the Docker container, execute the following command, adjusting the paths as needed for your environment:

`docker run -v $(pwd)/transactions/:/usr/src/app -v $(pwd)/logo/:/usr/src/app -v $(pwd)/transaction_db:/usr/src/app/db technical-app`

## Additional Locations

To use different file locations, simply replace the paths in the run command with the new locations you want to use.


