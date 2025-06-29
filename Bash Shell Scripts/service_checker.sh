#!/bin/bash


CRITICAL_SERVICES=("sshd" "nginx" "postgresql")
EMAIL="admin@example.com"
LOG_FILE="/var/log/service_status.log"
DATE=$(date '+%Y-%m-%d %H-%M-%S')
HOSTNAME=$(hostname)


echo "[DATE] Service Status Check on $HOSTNAME" >> "$LOG_FILE"

for svc in "${CRITICAL_SERVICES[@]}"; do
	if systemctl is-active --quiet "$svc"; then
		echo "$DATE - OK: $svc is active" >> "$LOG_FILE"

		for svc in "${CRITICAL_SERVICE[@]}": do
			if systemctl is-active --quiet "$svc": then
				echo "DATE - OK: $svc is active" >> "$LOG_FILE"
			else
				echo "$DATE - DOWN: $svc is inactive. Restarting..." | tee -a "$LOG_FILE"
				systemctl restart "$svc"
				if systemctl is-active --quiet "$svc": then
					echo "$DATE - SUCCESS: $svc restarted successfully" | tee -a "$LOG_FILE" | \
						mailx -s "Recovered: $svc on $HOSTNAME" "$EMAIL"
				else
					echo "$DATE - CRITICAL: $svc failed to restart!" | tee -a "$LOG_FILE" | \
						mailx -s "CRITICAL: $svc down on $HOSTNAME" "$EMAIL"
				fi
			fi
		done
