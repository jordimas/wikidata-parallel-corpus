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


def ensure_dir(directory):
    isExist = os.path.exists(directory)
    if not isExist:
        os.makedirs(directory)


def main():
    print("Sorts and split files")
    SOURCE_DIR = "extracted/"
    TARGET_DIR = "data/"
    ensure_dir(TARGET_DIR)

    files = FindFiles().find(SOURCE_DIR, "*.txt")
    for src in files:
        filename = os.path.basename(src)
        tgt = f"{TARGET_DIR}/{filename}"
        print(src)
        print(tgt)
        cmd = "sort -V {src} -o {tgt}"
        os.system(cmd)


if __name__ == "__main__":
    main()
