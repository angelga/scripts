#!/bin/bash
#
# Backup personal files
#
# find . -depth -mindepth 1 -maxdepth 1 -exec rm -rf {} \;

if [ "$#" -ne 1 ]; then
	echo "Usage: backup.sh destination_path"
	exit 1
fi

if [ ! -d "$1" ]; then
	echo "Destination directory doesn't exist: $1"
	exit 1
fi

# expand destination path
DEST_PATH=`cd "$1"; pwd`
HOME_PATH=`cd ~; pwd`

if [ "$DEST_PATH" = "$HOME_PATH" ]; then
	echo "Destination cannot be the home directory"
	exit 1
fi

echo "Archiving to $DEST_PATH"
pushd ~

echo "Archiving Keychains"
sudo cp "/Library/Keychains/System.keychain" "/var/db/SystemKey" $DEST_PATH
sudo chown $USER "$DEST_PATH/System.keychain" "$DEST_PATH/SystemKey"

sudo find /Users -type d -mindepth 1 -maxdepth 1 -not -iname "shared" -exec sh -c \
	'dirname_only=`basename "$0"`; mkdir "$1"/$dirname_only; \
	cp "$0"/Library/Keychains/*.keychain "$1"/$dirname_only; \
	chown -R "$2" "$1"/$dirname_only' \
	{} $DEST_PATH $USER \;

echo "Archiving dot files"
#TODO don't overwrite if existing
rsync -a ~/.bash_profile "$DEST_PATH"
rsync -a ~/.inputrc "$DEST_PATH"
rsync -a ~/.ssh "$DEST_PATH"

echo "Done"
popd