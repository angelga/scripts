#!/bin/bash
#
# Backup personal files
#

if [ "$#" -ne 1 ]; then
	echo "Usage: backup.sh destination_path"
	exit 1
fi

if [ ! -d "$1" ]; then
	echo "Destination directory doesn't exist: $1"
	exit 1
fi

echo "Archiving to $1"

rsync -av ~/.password-store "$1"
rsync -av ~/.inputrc "$1"
rsync -av ~/.gnupg "$1"
rsync -av ~/.profile "$1"
rsync -av ~/.ssh "$1"