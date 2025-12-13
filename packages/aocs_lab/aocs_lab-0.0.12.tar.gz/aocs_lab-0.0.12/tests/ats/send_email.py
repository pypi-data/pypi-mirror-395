import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, sender_password, recipient_email, subject, message):
    """
    Sends an email with the specified subject and message to the recipient_email.
    """
    try:
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Connect to the 126 SMTP server and send the email
        with smtplib.SMTP('smtp.126.com', 25) as server:  # Updated to use 126 email server
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def send_email_from_126(message):
    """
    Sends an email with the specified message using the 126 email server.
    """
    sender_email = "wzhmwz@126.com"
    sender_password = "BHpDBnvkpHZhPcMs"
    recipient_email = "wangzhao@yinhe.ht"
    subject = "Test Email"
    # message = "This is a test email 3."

    result = send_email(sender_email, sender_password, recipient_email, subject, message)
    print(result)


if __name__ == "__main__":
    send_email_from_126("hello world")
