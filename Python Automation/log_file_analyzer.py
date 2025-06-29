#!/usr/bin/env python3

import re
import os
import sys
from collections import Counter
from datetime import datetime

LOG_FILE = "/var/log/auth.log"

FAILED_LOGIN_PATTERN = r"Failed password.*from\s+(\d\.\d+\.\d+)"

def analyze_log(file_path):
    if not os.path.exits(file_path):
        print(f"Log file does not exist: {file_path}")
        sys.exit(1)
    with open(file_path, "r") as f:
        log_data = f.read()


    ip_list = re.findall(FAILED_LOGIN_PATTERN, log_date)

    ip_counter = Counter(ip_list)

    return ip_counter

def print_report(ip_counter, top_n=5):

    print("\n===== SSH Failed Login Report =====")
    print(f"Generate at: {datetime.now()}")
    print("-----------------------------------")
    print(f"{'IP Address':<20} {'Attempts':<10}")
    print("------------------------------------")

    for ip, count in ip_counter.most_common(top_n):
        print(f"{ip:<20} {count:<10}")

    print("-----------------------------------")
    print(f"Total Unique offenders: {len(ip_counter)}")
    print("====================================\n")

def main():

    custom_log = sys.argv[1] if len(sys.argv) > 1 else LOG_FILE
    ip_stats = analyze_log(custom_log)
    print_report(ip_stats)

if __name__ == "__main__":
    main()
