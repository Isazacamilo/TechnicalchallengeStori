import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from config import FROM, TO, SMTP_USERNAME, PASSWORD, LOGO, RECIPIENT


def send_notification(average_debit, average_credit, total_balance, year_month_with_transactions):

    multipart_message = MIMEMultipart("related")
    

    email_content = f"""<p style="font-size: 16px; font-weight: bold;">Dear {RECIPIENT},</p>
    <p style="font-size: 14px;">Hopes this email finds you in good health. We appreciate your continued trust in Stori, and we are pleased to provide you with your bank account statement for the ongoing year.</p>
    <p style="font-size: 14px;">Here is an overview of your account activity:</p>
    <p style="font-size: 14px; font-weight: bold;">Total Balance:</p>
    <p style="font-size: 14px;">Your current account balance is $ {total_balance:.2f}. This represents the total funds available in your account.</p>
    <p style="font-size: 14px; font-weight: bold;">Monthly Transactions:</p>
    
    """
    monthly_transaction_content = ""

    for month, transaction_data in year_month_with_transactions:
        monthly_transaction_content += f'<p style="font-size: 14px;">Number of transactions in {month}: {transaction_data}</p>'

    email_content += monthly_transaction_content
    email_content += f"""<p style="font-size: 14px;">Average Debit Amount:$ {average_debit:.2f}</span></p>
    <p style="font-size: 14px;">Average Credit Amount:$ {average_credit:.2f}</span></p>
    <p style="font-size: 14px;">This statement provides a comprehensive view of your account's financial activity, allowing you to monitor your transactions and manage your finances effectively.
    If you have any questions or concerns regarding your account statement or any other doubt, please do not hesitate to contact our dedicated customer support team at Stori. We are here to assist you.
    Thank you for choosing Stori as your trusted financial partner. We look forward to continuing to serve you and meet your banking needs.</p>
    <p style="font-size: 14px;">Sincerely</span></p>

    <img src="https://transactionaccount.s3.us-east-2.amazonaws.com/stori.png" alt="Embedded Image" style="display: block; margin-top: 10px;" />"""
    # <img src="cid:image_cid" alt="Embedded Image" style="display: block; margin-top: 10px;" />
    
    text_part = MIMEText(email_content, "html")
    multipart_message.attach(text_part)

    # with open("./logo/stori.png", "rb") as image_file:
    #     image = MIMEImage(image_file.read(), name="stori.png")
    #     image.add_header("Content-ID", "<image_cid>")
    #     multipart_message.attach(image)
    
    multipart_message["Subject"] = "Your Stori transaction summary for curent year"
    multipart_message["From"] = FROM
    multipart_message["To"] = TO

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = SMTP_USERNAME
    smtp_password = PASSWORD

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(
                multipart_message["From"],
                multipart_message["To"],
                multipart_message.as_string(),
                )
            print("Email sent successfully")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
