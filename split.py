import ijson
import sys
import datetime
import operator
import os
import fnmatch


class FindFiles(object):
    def find(self, directory, pattern):
        filelist = []

        for root, dirs, files in os.walk(directory):
            for basename in files:
                if fnmatch.fnmatch(basename, pattern):
                    filename = os.path.join(root, basename)
                    filelist.append(filename)

        filelist.sort()
        return filelist

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def ensure_dir(directory):
    isExist = os.path.exists(directory)
    if not isExist:
        os.makedirs(directory)


def main():
    print("Sorts and split files")
    SOURCE_DIR = "extracted/"
    TARGET_DIR = "data/"
    ensure_dir(TARGET_DIR)


    # Sort files
    sorted_files = []
    files = FindFiles().find(SOURCE_DIR, "*.txt")
    for src in files:
        filename = os.path.basename(src)
        tgt = os.path.join(TARGET_DIR, filename.replace(".txt", ".sorted"))
        sorted_files.append(sorted_files)
        cmd = f"sort -V {src} -o {tgt}"
        os.system(cmd)
        
            
        
if __name__ == "__main__":
    main()
