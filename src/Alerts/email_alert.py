import smtplib
from email.mime.text import MIMEText

EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
EMAIL_RECEIVER = "receiver@gmail.com"


def send_email_alert(message):
    try:
        msg = MIMEText(message)
        msg["Subject"] = "🚨 IDS Alert: Intrusion Detected"
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        print("[INFO] Email alert sent")

    except Exception as e:
        print(f"[ERROR] Email failed: {e}")