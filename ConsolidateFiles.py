__author__ = 'angel'

import operator
import os
import sys
import shutil

image_exts = ['jpg', 'png', 'gif']
video_exts = ['mp4', '3gp', 'wmv', 'avi', 'mpg', 'mpeg', 'flv', 'webm']


def get_file_extensions(search_path):
    dirs = 0
    images = 0
    videos = 0
    total = 0
    extensions = {}
    paths = [search_path]
    unknown_exts = []

    while len(paths) > 0:
        working_path = paths[0]
        paths.remove(working_path)
        for name in os.listdir(working_path):
            if name.startswith('.'):
                continue
            name = name.lower()
            fullname = os.path.join(working_path, name)
            if os.path.isdir(fullname):
                dirs += 1
                paths.append(fullname)
            else:
                tokens = fullname.split('.')
                if len(tokens) > 1:
                    ext = tokens[-1]
                    if not extensions.has_key(ext):
                        extensions[ext] = 0
                    extensions[ext] += 1

                    total += 1
                    if ext in image_exts:
                        images += 1
                    elif ext in video_exts:
                        videos += 1
                    else:
                        if not ext in unknown_exts:
                            unknown_exts.append(ext)

    print "Directories found: %d." % dirs
    print "Images found: %d." % images
    print "Videos found: %d." % videos
    print "Total files: %d. Missing files: %d." % (total, total - videos - images)
    if len(unknown_exts) > 0:
        print "Unknown file types: ",
        print unknown_exts
    sorted_extensions = sorted(extensions.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_extensions

def move_files(search_path, dest_path):
    paths = [search_path]
    image_path = os.path.join(dest_path, "images")
    video_path = os.path.join(dest_path, "videos")

    while len(paths) > 0:
        working_path = paths[0]
        paths.remove(working_path)
        for name in os.listdir(working_path):
            if name.startswith('.'):
                continue
            name = name.lower()
            fullname = os.path.join(working_path, name)
            if os.path.isdir(fullname):
                paths.append(fullname)
            else:
                tokens = fullname.split('.')
                if len(tokens) > 1:
                    ext = tokens[-1]

                    if ext in image_exts:
                        move_path = image_path
                    elif ext in video_exts:
                        move_path = video_path
                    else:
                        print "Unknown file %s" % fullname
                        continue

                    if not os.path.exists(move_path):
                        os.mkdir(move_path)
                    dest_finame = os.path.join(move_path, name)
                    if os.path.exists(dest_finame):
                        if os.stat(fullname).st_size == os.stat(dest_finame).st_size:
                            print "Remove file %s" % fullname
                            os.remove(fullname)
                    else:
                        shutil.move(fullname, move_path)

def remove_empty_dirs(search_path):
    paths = [search_path]
    paths_to_remove = []

    while len(paths) > 0:
        working_path = paths[0]
        paths.remove(working_path)
        for name in os.listdir(working_path):
            if name.startswith('.'):
                continue
            name = name.lower()
            fullname = os.path.join(working_path, name)
            if os.path.isdir(fullname):
                paths.append(fullname)
                if os.path.exists(os.path.join(fullname, ".DS_Store")):
                    os.remove(os.path.join(fullname, ".DS_Store"))
                if len(os.listdir(fullname)) == 0:
                    paths_to_remove.append(fullname)

    for empty_dir in paths_to_remove:
        print "Deleting dir: %s" % empty_dir
        os.rmdir(empty_dir)

if __name__ == '__main__':
    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)

    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = raw_input("Path to scan: ")

    if not os.path.exists(path):
        print "Path doesn't exist"
        sys.exit()

    exts = get_file_extensions(path)
    for ext, frequency in exts:
        print "Files for .%s: %d." % (ext, frequency)

    if len(sys.argv) > 2:
        dest = sys.argv[2]
        if not os.path.exists(dest):
            print "Destination doesn't exist"
            sys.exit()

        print "Moving files from %s to %s" % (path, dest)
        move_files(path, dest)
        remove_empty_dirs(path)