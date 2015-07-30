__author__ = 'angel'

import sys
import os
import shutil


ignore_extensions = ["aae"]


class Picture:

    def __init__(self, path, filename, size):
        self.path = path
        self.filename = filename
        self.size = size

    def __eq__(self, other):
        return self.path != other.path and self.filename == other.filename and self.size == other.size

    def __repr__(self):
        return "Picture({0.filename!r}, {0.size!r}, {0.path!r})".format(self)


def get_files(path):
    files = []
    paths = [path]

    while len(paths) > 0:
        working_path = paths[0]
        paths.remove(working_path)
        for filename in os.listdir(working_path):
            full_filename = os.path.join(working_path, filename)

            if filename.startswith('.'):
                print "Ignoring file: %s." % full_filename
                continue

            if os.path.isdir(full_filename):
                paths.append(full_filename)
            else:
                tokens = filename.split('.')
                if len(tokens) > 1:
                    ext = tokens[-1]

                    if ext in ignore_extensions:
                        continue

                picture = Picture(working_path, filename, os.stat(full_filename).st_size)
                files.append(picture)

    return files


if __name__ == '__main__':
    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)

    if len(sys.argv) != 3:
        print "Usage: syncpics.py source dest"
        sys.exit()

    source = sys.argv[1]

    if not os.path.exists(source):
        print "Source path doesn't exist"
        sys.exit()

    destination = sys.argv[2]

    if not os.path.exists(destination):
        print "Destination path doesn't exist"
        sys.exit()

    source_files = get_files(source)

    destination_files = get_files(destination)

    same_pics = []

    for source_file in source_files:
        found = False
        for dest_file in destination_files:
            if source_file.__eq__(dest_file):
                same_pics.append("File '{0}' in {1} = {2}.".format(source_file.filename, source_file.path, dest_file.path))
                found = True

        if not found:
            if os.path.exists(os.path.join(destination, source_file.filename)):
                print "Error file does exist in destination: %s." % source_file.filename
                sys.exit()
            full_source_path = os.path.join(source_file.path, source_file.filename)
            full_dest_path = os.path.join(destination, source_file.filename)
            print "Copying '%s' to '%s'" % (full_source_path, destination)
            shutil.copyfile(full_source_path, full_dest_path)