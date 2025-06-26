#!/usr/bin/env python3

import psutil
import logging
import smtplib
from email.message import EmailMessage
from datetime import datetime


THRESHOLD = 80
ALERT_EMAIL = "admin@example.com"
SMTP_SERVER = "localhost"
LOG_FILE = "/var/log/disk_usage_reporter.log"


logging.basicConfig(filename=LOG_FILE,level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')


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
        logging.error(f"Failed to end email: {e}")


def check_disk_usage(threshold=THRESHOLD):

    partitions = psutil.disk_partitions(all=False)
    alert_lines = []
    report_lines = []

    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue

        percent = usage.percent
        total_gb = usage.total / (1024 ** 3)
        used_gb = usage.used / (1024 ** 3)
        free_gb = usage.free / (1024 ** 3)

        line = (f"{partition.mountpoint:<15} Total: {total_gb:.1f} GB " f"Used: {used_gb:.1f} GB Free: {free_gb:.1f} GB " f"Usage: {percent}%")
        report_lines.append(line)

        if percent >= threshold:
            alert_lines.applend(f"High disk usage on {partition.mountpoint}: {percent}%")
    return report, alert_lines


def main():
