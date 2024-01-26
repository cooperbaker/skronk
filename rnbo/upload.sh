# upload rnbo setup files onto the raspberry pi via rsync

USERNAME="pi"
HOSTNAME="skronk"

rsync --delete --times --perms --verbose --archive --recursive --group --human-readable --progress --exclude "upload.sh" ../rnbo "$USERNAME"@"$HOSTNAME":/home/pi/
