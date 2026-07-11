import smtplib
from email.mime.text import MIMEText
from config import Config

def send_email(to_email, subject, body):

    if not Config.MAIL_USERNAME or not Config.MAIL_PASSWORD:
        return

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = Config.MAIL_USERNAME
    msg["To"] = to_email

    try:
        server = smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT)
        server.starttls()
        server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)

        server.send_message(msg)
        server.quit()

        print("EMAIL SENT TO:", to_email)

    except Exception as e:
        print("EMAIL ERROR:", str(e))