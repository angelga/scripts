# Ensure user-installed binaries take precedence
export PATH=/usr/local/bin:$PATH
# Set architecture flags
export ARCHFLAGS="-arch x86_64"
# Load .bashrc if it exists
test -f ~/.bashrc && source ~/.bashrc

#
# Functions and aliases
#
yd()
{
	python ~/github/scripts/youtube-dl.py "$1" "$2"
}

ig()
{
    wget -qO - "$1" | grep og:image | grep -o 'https://[^"]*' | cut -d? -f1
}

igd()
{
    wget -qO - "$1" | grep og:image | grep -o 'https://[^"]*' | cut -d? -f1 | xargs wget -nv
}

alias lsa='ls -all'

mf()
{
	find . -iname "*$1*"
}

cdl()
{
	cd "$1" && ls
}

cdu()
{
	cd .. && ls
}

gitpush()
{
	git push origin master
}

alias newpost='python ~/github/scripts/newpost.py' 
alias hsclear='cat /dev/null > ~/.bash_history && history -cw && exit'
alias wgetdoc='wget -r -l5 -k -np -p'
alias filetree="ls -R | grep ":$" | sed -e 's/:$//' -e 's/[^-][^\/]*\//--/g' -e 's/^/ /' -e 's/-/|/'"
alias ptest="python -m unittest discover --pattern=*.py -v"

#
# Color settings
#
export CLICOLOR=1
export LSCOLORS=GxFxCxDxBxegedabagaced

#
# Settings for bash-completion
#
if [ -f $(brew --prefix)/etc/bash_completion ]; then
    source $(brew --prefix)/etc/bash_completion
fi

