__author__ = 'angel'

import os
import urlparse
import sys


if __name__ == '__main__':
    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)
    usage = "Usage: youtube-dl.py url -mp3"

    if len(sys.argv) == 1:
        print usage
        sys.exit()

    # Parse URL to later remove unwanted list ids, index, etc.
    url = sys.argv[1]
    if not url:
    	print usage
    	sys.exit(2)


    parsed_url = urlparse.urlparse(url)
    video_id = urlparse.parse_qs(parsed_url.query)['v'][0]

    vid = False
    if len(sys.argv) == 3:
        if sys.argv[2] == 'vid':
            vid = True

    # Only leave the v parameter
    short_url = parsed_url.scheme + "://" + parsed_url.hostname + parsed_url.path + "?v=" + video_id
    print "Downloading %s" % short_url

    # Command to be ran with new short url
    if not vid:
        cmd = "youtube-dl --extract-audio --audio-format mp3 " + short_url
    else:
        cmd = "youtube-dl " + short_url
    print "Command to run: %s" % cmd

    # Change to desktop to save songs there
    original_working_dir = os.getcwd()
    os.chdir(os.path.expanduser("~/Desktop"))
    print "Set working directory: %s" % os.getcwd()

    os.system(cmd)

    # Change to original path
    os.chdir(original_working_dir)
    print "Set directory back to: %s" % original_working_dir
