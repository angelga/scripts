export PATH=~/bin:$PATH
export EDITOR='subl -w'

export PATH="/usr/local/bin:$PATH"

youtube_download()
{
	python ~/desktop/github/scripts/youtube-dl.py $1
}

alias ytdl=youtube_download