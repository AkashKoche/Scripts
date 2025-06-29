#!/bin/bash

THRESHOLD=85
EMAIL="admin@example.com"
LOG_FILE="/var/log/disk_usage_daily.log"
DATE=$(date '+%Y-%m-%d %H:%M-%S')
HOSTNAME=$(hostname)


echo "===== Disk Usage Check at $DATE =====" >> "$LOG_FILE"


df -hP | grep '^/dev/' | while read -r line; do
    USAGE=$(echo $line | awk '{print $5}' | tr -d '%')
    FS=$(echo $line | awk '{print $6}')
    if [ "$USAGE" -ge "$THRESHOLD"]; then
	    echo "$DATE - ALERT: $FS is at ${USAGE}% on $HOSTNAME" | tee -a "$LOG_FILE" | \
		    mailx -s "Disk Alert: $FS ${USAGE}% Full on $HOSTNAME" "$EMAIL"
    else echo "DATE -OK: $FS is at ${USAGE}%" >> "$LOG_FILE"
    fi
done
