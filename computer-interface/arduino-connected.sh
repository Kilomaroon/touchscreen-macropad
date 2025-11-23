#!/bin/bash
# /usr/local/bin/arduino-connected.sh
# Script executed when Arduino is connected

DEVICE_PATH="$1"
LOG_FILE="/var/log/arduino-hotplug.log"

echo "$(date): Arduino connected at $DEVICE_PATH" >> "$LOG_FILE"

# Send notification to all logged-in users
for user in $(loginctl list-users --output json \
             | jq -r '.[] | .user') ; do
  systemd-run \
    --user \
    --machine=${user}@.host \
    notify-send \
       "Arduino Connected" "Device available at $DEVICE_PATH";
done


exit 0
