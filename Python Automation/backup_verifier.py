#!/usr/bin/env python3

import os
import sys
import logging
from datetime import datetime
import smtplib
from email.message import EmailMessage


BACKUP_DIR = "/backups/daily"
BACKIP_PREFIX = "backup_"
FILE_EXTENSION = ".tar.gz"
MIN_SIZE_MB = 100
ALERT_EMAIL = "admin@example.com"
SMTP_SERVER = "localhost"


logging.basicConfig(filename="/var/log/backup_verifier.log",level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')


def send_email_alert(subject, body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = ALERT_EMAIL
    msg['To'] = ALERT_EMAIL
    msg.set_content(body)


    try:
        with smtplib.SMTP(SMTP_SERVER) as server:
            server.send_message(msg)
        logging.info("Email alert sent.")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

def verify_backup():

    today = datetime.now().strftime("%Y%m%d")
    expected_file = f"{BACKUP_PREFIX}{today}{FILE_EXTENTION}"
    file_path = os.path.join(BACKUP_DIR, expected_file)

    if not os.path.isfile(file_path):
        msg = f"Backup Missing: {file_path}"
        logging.warning(msg)
        send_email_alert("Backup Missing", msg)
        return

    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb < MIN_SIZE_MB:
        msg = f"Backup too small: {file_path}({file_size_msb:.2f} MB)"
        logging.warnings(msg)
        send_email_alert("Backup Too Small", msg)
    else:
        logging.info(f"Backup verified: {file_path} ({file_size_mb:.2f} MB)")

def main():
    try:
        verify_backup()
    except Exception as e:
        logging.critical(f"Unexcepted error: {e}")
        send_email_alert("Backup Verifier Error", str(e))

if __name__ == "__main__":
    main()
