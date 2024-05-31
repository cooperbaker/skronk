#!/bin/bash

# sync python files onto the raspberry pi via rsync

USERNAME="pi"
HOSTNAME="skronk"

echo ""
echo -e "\033[1mSyncing Files to Raspberry Pi"
echo -e "\033[0m\033[1A"
echo ""

cd "$(dirname "$0")"

rsync --rsync-path="sudo rsync" --exclude "+sync.command" --exclude ".DS_Store" --delete --times --perms --verbose --archive --recursive --group --human-readable --progress ../skronk "$USERNAME"@"$HOSTNAME":/home/pi/

echo ""
echo -e "\033[1mSync Complete"
echo -e "\033[0m\033[1A"
echo ""

read -rsp $'Press any key to continue...\n' -n1 key
# sleep 3