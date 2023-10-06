import ijson
import sys
import datetime
import operator
import os


def ensure_dir(directory):
    isExist = os.path.exists(directory)
    if not isExist:
        os.makedirs(directory)


def inc_string_counter_for_lang(languages, language):
    counter = languages.get(language, 0) + 1
    languages[language] = counter


def create_file(directory, language, part, files):
    file_h = open(f"{directory}/{language}-{part}.raw", "w")
    files[language] = file_h
    return file_h


def extract(directory):
    start_time = datetime.datetime.now()

    items = ijson.items(sys.stdin, "item", use_float=True)
    languages = {}
    files = {}
    parts = {}
    processed = 0
    MAX_LINES = 500000
    for item in items:
        if processed % 1000000 == 0:
            print(f"item processed: {processed}")

        processed += 1

        _id = item.get("id")
        if not _id:
            continue

        descriptions = item.get("descriptions")
        for language in descriptions.keys():
            description = descriptions[language].get("value")
            if len(description) == 0:
                continue

            inc_string_counter_for_lang(languages, language)

            file_h = files.get(language)
            part, lines = parts.get(language, (1, 0))
            lines += 1

            if not file_h:
                file_h = create_file(directory, language, part, files)

            elif lines > MAX_LINES:
                lines = 0
                part += 1

                file_h.close()
                file_h = create_file(directory, language, part, files)

            file_h.write(f"{_id}\t{description}\n")
            parts[language] = (part, lines)

    #        if processed > 1000:
    #            break

    for language in parts:
        last_part = parts[language]
        for part in range(0, len(last_part)):
            src = f"{directory}/{language}-{part}.raw"
            tgt = f"{directory}/{language}-{part}.txt"
            if not os.path.exists(src):
                continue

            cmd = f"sort -V {src} -o {tgt}"
            os.system(cmd)

    s = sorted(languages.items(), key=operator.itemgetter(1), reverse=True)
    with open("languages.txt", "w") as f_output:
        for language, counter in s:
            pequal = counter * 100 / processed
            f_output.write(f"{language} - {counter} ({pequal:.2f}%)\n")

    s = "Time used: {0}".format(datetime.datetime.now() - start_time)
    print(s)


def main():
    directory = "data/"
    ensure_dir(directory)
    extract(directory)


if __name__ == "__main__":
    main()