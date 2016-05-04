#!/bin/bash
#
# Backup personal files
#
# Run for deleting test destination path:
#
#	find . -depth -mindepth 1 -maxdepth 1 -exec rm -rf {} \;
#

red=$'\e[1;31m'
grn=$'\e[1;32m'
yel=$'\e[1;33m'
blu=$'\e[1;34m'
mag=$'\e[1;35m'
cyn=$'\e[1;36m'
end=$'\e[0m'

usage()
{
	printf "%s\n" "${red}Usage:${end} $0 -d [destination] [-q]";
	echo "";
}

DESTINATION=
QUICK=

while getopts "hd:q" OPTION
do
	case $OPTION in
		h)
			usage
			exit 1
			;;
		d)
			DESTINATION=$OPTARG
			;;
		q)
			QUICK=1
			;;
		?)
			usage
			exit
			;;
	esac
done

if [ -z $DESTINATION ]
then
	usage
	exit 1
fi

if [ ! -d "$DESTINATION" ]; then
	printf "%s\n" "${red}Error:${end} destination directory doesn't exist: $DESTINATION"
	exit 1
fi

# expand destination path
DEST_PATH=`cd "$DESTINATION"; pwd`
HOME_PATH=`cd ~; pwd`

if [ "$DEST_PATH" = "$HOME_PATH" ]; then
	printf "%s\n" "${red}Error:${end} destination cannot be the home directory"
	exit 1
fi

printf "%s\n" "${grn}Archiving to $DEST_PATH${end}"
pushd ~

echo "Archiving system keychains"
sudo cp "/Library/Keychains/System.keychain" "/var/db/SystemKey" $DEST_PATH
sudo chown $USER "$DEST_PATH/System.keychain" "$DEST_PATH/SystemKey"

echo "Archiving user keychains"
sudo find /Users -type d -mindepth 1 -maxdepth 1 -not -iname "shared" -exec sh -c \
	'dirname_only=`basename "$0"`; mkdir "$1"/$dirname_only; \
	cp "$0"/Library/Keychains/*.keychain "$1"/$dirname_only; \
	chown -R "$2" "$1"/$dirname_only' \
	{} $DEST_PATH $USER \;

echo "Archiving dot files"
#TODO don't overwrite if existing
rsync -a ~/.inputrc "$DEST_PATH"
rsync -a ~/.bash_profile "$DEST_PATH"
rsync -a ~/.screenrc "$DEST_PATH"
rsync -a ~/.ssh "$DEST_PATH"
rsync -a ~/virtualenvs "$DEST_PATH"

echo "Archiving github repos"
rsync -a ~/github "$DEST_PATH"


if [ $QUICK ]; then
	printf "%s\n" "${grn}Quick backup completed${end}"
	exit
fi

echo "Archiving Desktop & Downloads"
rsync -a ~/Downloads "$DEST_PATH"
rsync -a ~/Desktop "$DEST_PATH"

echo "Archiving sync folder"
rsync -a ~/sync "$DEST_PATH"

printf "%s\n" "${grn}Archiving ... done${end}"
popd
