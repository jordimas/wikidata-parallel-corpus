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


def getfiname(original, part, directory):
    _file = original.replace(".txt", "")
    filename = f"{_file}-{part}.txt"
    return os.path.join(directory, filename)


def main():
    print("Sorts and split files")
    SOURCE_DIR = "extracted/"
    TARGET_DIR = "data/"
    ensure_dir(TARGET_DIR)

    # Sort files
    sorted_filename = []
    sorted_fullpath = []
    files = FindFiles().find(SOURCE_DIR, "*.txt")
    for src in files:
        filename = os.path.basename(src)
        sorted_filename.append(filename)
        tgt = os.path.join(TARGET_DIR, filename.replace(".txt", ".sorted"))
        sorted_fullpath.append(tgt)
        cmd = f"sort -V {src} -o {tgt}"
        os.system(cmd)

    MAX_LINES = 1000000
    for fullpath, filename in zip(sorted_fullpath, sorted_filename):
        part = 1
        with open(fullpath, "r") as fh_input:
            lines = 0
            output_file = getfiname(filename, part, TARGET_DIR)
            fh_output = open(output_file, "w")
            while True:
                src = fh_input.readline()
                fh_output.write(src)

                if not src:
                    break

                if lines > MAX_LINES:
                    lines = 0
                    fh_output.close()
                    part += 1

                    output_file = getfiname(filename, part, TARGET_DIR)
                    fh_output = open(output_file, "w")

                lines += 1


if __name__ == "__main__":
    main()
