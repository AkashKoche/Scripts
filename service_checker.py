#!/usr/bin/env python3

import subprocess
import logging
import smtplib
from email.message import EmailMessage
from datetime import datetime


SERVICES = ["sshd", "nginx", "mysql"]
LOG_FILE = "/var/log/service_checker.log"
EMAIL = "admin@example.com"
SMTP_SERVER = "localhost"


logging.basicConfig(filename=LOG_FILE,
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


def is_service_active(service_name):
    try:
        result = subprocess.run(
                ["systemctl", "is-active", service_name],
                capture_output=True, text=True, check=False
                )
        return result.stdout.strip() == "active"
    exept Exception as e:
        logging.error("Error checking {service_name}: {e}")
        return False


def restart_service(service_name):
    try:
        subprocess.run(
                ["systemctl", "restart", service_name],
                capture_output=True, text=True, check=True
                )
        logging.info(f"Restarted service: {service_name}")
        return True
    except subprocess.CalledProcessError a e:
        logging.error(f"Failed to restart {service_name}: {e.stderr}")
        return False


def send_alert(service_name, message):
    msg = EmailMessage()
    msg['Subject'] = f"Service Alert: {service_name} on {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    msg['From'] = EMAIL
    msg['TO'] = EMAIL
    msg.set_content(message)


    try:
        with smtplib.SMTP(SMTP_SERVER) as server:
            server.send_message(msg)
            logging.info(f"Alert email sent for service: {service_name}")
    except Exception as e:
        logging.error(f"Failed to send email for {service_name}: {e}")


def check_services():
    for service in SERVICES:
        if is_service_active(service):
            logging.info(f"{service} is active")
        else:
            logging.waring(f"{service} is down. Attempting restart.")
            restarted = restart_service(service)
            if not restarted:
                msg = f"{service} is down and failed to restart on {datetime.now()}."
                send_alert(service, msg)


def main():
    logging.info("Running service checker...")
    check_services()


if __name__ == " __main__ ":
    main()
