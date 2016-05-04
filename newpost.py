#!/usr/bin/env python
import random
import sys, getopt, os
from datetime import date

def print_usage(msg, code=0):
	usage = 'dice.py -t <post title> -n <filename>'
	if msg:
		print msg
	print usage
	sys.exit(code)
	
def main(argv):
    title = ''
    name = ''

    try:
        opts, args = getopt.getopt(argv,"ht:n:",["help","title=","name="])
    except getopt.GetoptError as error:
        print_usage(error, 2)

    for opt, arg in opts:
        if opt == '-h':
	    print_usage(None)
        elif opt in ("-t", "--title"):
            title = arg
	elif opt in ("-n", "--name"):
	    name = arg
        else:
	    print_usage("Unknown argument: %s" % opt, 2)

    if not title:
	    print_usage("Title is required", 2)
    if not name:
	    print_usage("Filename is required", 2)

    file_path = "/Users/angel/github/mysite/content/"
    if not os.path.exists(file_path):
	    print_usage("Path does not exist: %s" % file_path, 2)
    if not os.path.isdir(file_path):
            print_usage("Path not folder: %s" % file_path, 2)
    file_path = os.path.join(file_path, name)
    if not os.path.splitext(file_path)[1].lower() == ".md":
	    file_path += ".md"
    if os.path.exists(file_path):
	    print_usage("File already exists: %s" % file_path, 2)

    post_date = date.today().isoformat()
    print "Name: %s. Date: %s. Title: %s." % (name, post_date, title)
    with open(file_path, "w") as f:
	    f.write("Title: %s\n" % title)
	    f.write("Date: %s\n" % post_date)
	    f.write("Tags: \n")
	    f.close()

if __name__ == "__main__":
    main(sys.argv[1:])
