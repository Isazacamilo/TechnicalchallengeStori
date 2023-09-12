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


## AWS configuration S3, ECR and Lambda from AWS CLI

For this challenge we are going to use S3 bucket to contain the account CSV and the Stori logo. An ECR to allow the deploy of a Docker image with the code and finally a Lambda fucntion that will run based on a docker image uploaded.

### S3:
Create and configure a S3 bucket as public (we are doing public just for challenge excersise).

https://s3.console.aws.amazon.com/s3/bucket/create?region=us-east-1

Leave Object Ownership as ACLs disable (recommended).

Block Public Access settings for this bucket:
- Uncheck Block all public access
- Check the acknowledge warning 
- Leave other settings as default
- Click create bucket

Navigate and access the bucket, click on permissions tab. In Bucket policy add a ReadPublic policy.

Example:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicRead",
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject",
                "s3:GetObjectVersion"
            ],
            "Resource": "arn:aws:s3:::<Your-bucket-name>/*"
        }
    ]
}

```

### ECR:

Create and configure an ECR.

https://us-east-1.console.aws.amazon.com/ecr/create-repository?region=us-east-1

Provide a name for your repository and click on create repository.

NOTE: It will looks like 197012199319.dkr.ecr.us-east-1.amazonaws.com/<Your-repository-name>

### AWS CLI

If you don't have AWS CLI, download it from here:

https://docs.aws.amazon.com/es_es/cli/latest/userguide/getting-started-install.html

From AWS UI go to Security credencials and created an Access Key:

- Save Access key in a notepad
- save Secret access key in a notepad


Click in Done to complete creation of Access Key.

# Configuring your CLI on your local machine

On your command line (CMD in my case because I'm using windows, commands may change base on the OS)

Run following command:

- Verify that AWS CLI was correctly installed `aws --version` (If you don't get a version, repeat CLI installation step)
- Run aws configuration `aws configure`
- Paste the access key and secret access key that you have in the notepad
- Complete the info that CMD will ask

Example:

```
C:\Users\User>aws configure
AWS Access Key ID [None]: <your-access-key>
AWS Secret Access Key [None]: <your-secret-access-key>
Default region name [None]: us-east-2 ------> aws zone
Default output format [None]: json 

```

