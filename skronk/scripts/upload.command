#!/bin/bash
#-------------------------------------------------------------------------------
# upload.sh
#
# Skronk Firmware Development Upload Script
# Ryncs all Skronk files onto the Raspberry Pi
# See README.md for install instructions
#
# Cooper Baker (c) 2024
# http://nyquist.dev/skronk
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# login info
#-------------------------------------------------------------------------------
USERNAME="pi"
HOSTNAME="skronk"

#-------------------------------------------------------------------------------
# upload skronk
#-------------------------------------------------------------------------------
echo ""
echo -e "\033[1mUploading Skronk"
echo -e "\033[0m\033[1A"
echo ""


#-------------------------------------------------------------------------------
# sync files
#-------------------------------------------------------------------------------
echo -e "\033[1mSyncing Files..."
echo -e "\033[0m\033[1A"
echo ""
cd "$(dirname "$0")"
cd ../../..
rsync --exclude "upload.command" --exclude ".*" --exclude "__pycache__" --delete --times --perms --verbose --archive --recursive --group --human-readable --progress ./skronk "$USERNAME"@"$HOSTNAME":/home/pi/
echo ""

#-------------------------------------------------------------------------------
# upload complete
#-------------------------------------------------------------------------------
echo -e "\033[1mUpload Complete"
echo -e "\033[0m\033[1A"
echo ""
read -rsp $'Press any key to continue...\n' -n1 key


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
