# Account CSV Reader

The Account CSV Reader is a project designed to read an account CSV file and send an email to the user containing their account balance and a summary of the number of transactions for each month.

# Assumptions

- Account file has information from curent year
- File has same structure as the example: Id,Date,Transaction
- There are no month's with transactions with values 0
- Date column has month first and second day


## Configuration
To run the project locally, you need to configure a .env file with the following variables:
- FILE: The path to the CSV file containing account data (e.g., "transactions/account.csv").
- LOGO: The path to the logo file you want to include in the email (e.g., "./logo/stori.png").
- PASSWORD: The SMTP password for the email account used to send emails.
- SMTP_USERNAME: The SMTP username or email address for the email account.
- FROM: The email address from which the email will be sent.
- TO: The recipient's email address.
- DB_URL = "transaction_account.db" This can be the name of the DB that you want to create, just need to add the name.db

Make sure to replace these example values with your actual configuration.

## How to Run

To build the Docker image, use the following command, replacing <name that you want> with your desired image name:

`docker build -t <name-that-you-want> .`

To run the Docker container, execute the following command, adjusting the paths as needed for your environment:

`docker run  <name-that-you-put-in-the-build>`

NOTE: If the .env that you created is not in same level of app.py or if you want to put the account.csv and logo in diferent locations, is possible that you need to add Volumes to the docker run command. If you want to check the db file that code will create you will need to run the container in interactive mode: docker run -it <name-of-your-container-image>

## Check DB

This project is creating a SQLite db to show the data, if you want to check how is the data inserted and showed in the db, you can install an extension in Visual Studio code to view the db. Extension name: SQLite

NOTE: Once db file is created after running your code in local (not using container) you can right click and elect Open DataBase, that will open a SQLite Explorer and then you can right click and view the table.

Example of the DB after Inserting data:


|id|	      date	       |          money       |	transaction_type|
|:--:|:-----------------------:|:------------:|:-------------------:| 
|1 |	2023-02-15 00:00:00|	45.67	|Debit              |
|2 |	2023-02-25 00:00:00|	-15.75	|Credit             |
|3 |	2023-04-20 00:00:00|	23.2	|Debit              |
|4 |	2023-05-19 00:00:00|	-100.6  |Credit             |
|5 |	2023-06-09 00:00:00|	400.6	|Debit              |


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

### Configuring your CLI on your local machine

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

After that process run following commands:

`aws configure export-credentials --format env`

- Copy the files that command return into a notepad and run it one by one

`export AWS_ACCESS_KEY_ID=<your-access-key>`
`export AWS_SECRET_ACCESS_KEY_ID=<your-secret-access-key>`

### Login to ECR

Run the command to login to ECR from your local:

`aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 197012199319.dkr.ecr.us-east-1.amazonaws.com/<your-repository-name>`

197012199319.dkr.ecr.us-east-1.amazonaws.com/<your-container-name>  ------> Replace with your actual link from ECR and repository name

### Build image

NOTE: Make sure to remove .env from the actual directory in which you are running the build (envs variables will be configured in the Lambda)

`docker build -t <same-name-as-ECR-repository> .`

### Tag image

`docker tag <same-name-as-ECR-repository>:latest 197012199319.dkr.ecr.us-east-1.amazonaws.com/<same-name-as-ECR-repository>:latest`

### Push image to ECR

`docker push 197012199319.dkr.ecr.us-east-1.amazonaws.com/<same-name-as-ECR-repository>:latest`

### Lambda

Create a Lambda function using container image option:

https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/create/function?intent=authorFromImage

Give a name to the function (recomendation same name as ECR repository).

- Click on Browse image and the image that you pushed should be there.
- Click create function.
- Access the function and go to configuration -----> Environmental variables.
- Add all the variables.
- Click on Image ------> Implement new image and select the latest one.
- Wait until image load and the test the lambda

If all is fine you should get all the messages in the log on the lambda and an mail in the email that you set in the TO env variable.

