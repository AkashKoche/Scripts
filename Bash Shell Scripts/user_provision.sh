#!/bin/bash

CSV_FILE="$1"
LOG_FILE="/var/log/user_provision.log"
DEFAULT_SHELL="/bin/bash"
DEFAULT_PASS_EXPIRY=30


if [ ! -f "$CSV_FILE" ]; then
	echo "ERROR: CSV file not found: $CSV_FILE"
	exit 1
fi


while IFS=',' read -r username fullname; do
	if id "$username" &>/dev/null; then
		echo "$(date): User $username already exists. Skipping." >> "$LOG_FILE"
	else
		useradd -m -s "$DEFAULT_SHELL" -c "$fullname" "$username
		echo "$username:Welcome@123 | chpasswd
		chage -M $DEFAULT_PASS_EXPIRY "$username"
		echo "$(date): Created user $username ($fullname) with default password and expiry" >> "$LOG_FILE"
	fi
done < "$CSV_FILE"
