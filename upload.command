#!/bin/bash

# rsync skronk files onto the raspberry pi

USERNAME="pi"
HOSTNAME="skronk"

echo ""
echo -e "\033[1mSyncing Files to Raspberry Pi"
echo -e "\033[0m\033[1A"
echo ""

cd "$(dirname "$0")"

rsync --rsync-path="rsync" --exclude "upload.command" --exclude ".*" --exclude "__pycache__" --delete --times --perms --verbose --archive --recursive --group --human-readable --progress ./skronk ./pd "$USERNAME"@"$HOSTNAME":/home/pi/

echo ""
echo -e "\033[1mSync Complete"
echo -e "\033[0m\033[1A"
echo ""

read -rsp $'Press any key to continue...\n' -n1 key