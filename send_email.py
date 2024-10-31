import smtplib
import time
import schedule
import os
from decouple import config


SMTP_SERVER = config('SMTP_SERVER')
SMTP_PORT = config('SMTP_PORT', cast=int) 
EMAIL_ADDRESS = config('EMAIL_ADDRESS')
EMAIL_PASSWORD = config('EMAIL_PASSWORD')
TO_EMAIL_ADDRESS = config('TO_EMAIL_ADDRESS')
LOG_FILE_PATH = config('LOG_FILE_PATH')


def send_email():
    # Read the log file
    if os.path.exists(LOG_FILE_PATH):
        with open(LOG_FILE_PATH, "rb") as log_file:
            log_data = log_file.read()

        subject = "Honeypot Logs"
        body = "Attached are the latest logs from the honeypot."
        message = f"Subject: {subject}\n\n{body}".encode() + log_data

        try:
            # Setup the server
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls() 
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.sendmail(EMAIL_ADDRESS, TO_EMAIL_ADDRESS, message)
            print(f"[INFO] Email sent successfully to {TO_EMAIL_ADDRESS}")
        except Exception as e:
            print(f"[ERROR] Failed to send email: {e}")
    else:
        print(f"[ERROR] Log file not found: {LOG_FILE_PATH}")


# Schedule the email sending every 5 minutes
schedule.every(1).minutes.do(send_email)

if __name__ == "__main__":
    print("[INFO] Starting email scheduler...")
    while True:
        schedule.run_pending()
        time.sleep(1)
