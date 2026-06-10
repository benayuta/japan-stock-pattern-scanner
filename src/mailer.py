import smtplib

from email.mime.text import MIMEText

from config import (
    GMAIL_USER,
    GMAIL_APP_PASSWORD
)

def send_mail(body):

    msg = MIMEText(body)

    msg["Subject"] = "日本株パターンスキャン"
    msg["From"] = GMAIL_USER
    msg["To"] = GMAIL_USER

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            GMAIL_USER,
            GMAIL_APP_PASSWORD
        )

        smtp.send_message(msg)
