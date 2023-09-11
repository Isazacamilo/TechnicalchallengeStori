import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from config import FROM, TO, SMTP_USERNAME, PASSWORD, LOGO


def send_notification(
    average_debit, average_credit, total_balance, year_month_with_transactions
):
    recipient_name = "Camilo"

    multipart_message = MIMEMultipart("related")

    email_content = f"""<p style="font-size: 16px; font-weight: bold;">Hello {recipient_name},</p>
    <p style="font-size: 14px;">Following email is to inform you and show your transactions within this current year:</p>
    <p style="font-size: 14px;">Total balance is:${total_balance:.2f}</span></p>"""
    monthly_transaction_content = ""

    for month, transaction_data in year_month_with_transactions:
        monthly_transaction_content += f'<p style="font-size: 14px;">Number of transactions in {month}: {transaction_data}</p>'

    email_content += monthly_transaction_content
    email_content += f"""<p style="font-size: 14px;">Average debit amount:${average_debit:.2f}</span></p>
    <p style="font-size: 14px;">Average credit amount:${average_credit:.2f}</span></p>
    <p style="font-size: 14px;">Please let us know if you have any type of concern.</p>
    <p style="font-size: 14px;">Regards,</p>
    <img src="cid:image_cid" alt="Embedded Image" style="display: block; margin-top: 10px;" />"""

    text_part = MIMEText(email_content, "html")
    multipart_message.attach(text_part)

    with open(LOGO, "rb") as image_file:
        image = MIMEImage(image_file.read(), name="stori.png")
        image.add_header("Content-ID", "<image_cid>")
        multipart_message.attach(image)

    multipart_message["Subject"] = "Transaction Summary"
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
