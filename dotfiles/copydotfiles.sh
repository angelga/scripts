#!/bin/bash
#
# Backup dotfiles
#

red=$'\e[1;31m'
grn=$'\e[1;32m'
yel=$'\e[1;33m'
blu=$'\e[1;34m'
mag=$'\e[1;35m'
cyn=$'\e[1;36m'
end=$'\e[0m'

# Ignore . and .. files
GLOBIGNORE=.:..
# Expand to null if pattern not found
shopt -s nullglob

for f in .*
do
    if [ -f ~/$f ] ; then
        if ! cmp -s $f ~/$f; then
            printf "${blu}Copying $f${end}\n"
            cp ~/$f .
        else
            printf "${yel}Ignoring $f${end}\n"
        fi
    fi
done

printf "${grn}Done${end}\n"
