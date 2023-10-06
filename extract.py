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


def extract(directory):
    start_time = datetime.datetime.now()

    items = ijson.items(sys.stdin, "item", use_float=True)
    languages = {}
    files = {}
    processed = 0
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

            if not file_h:
                file_h = open(f"{directory}/{language}.txt", "w")
                files[language] = file_h

            file_h.write(f"{_id}\t{description}\n")

        if processed > 5000000:
            break

    s = sorted(languages.items(), key=operator.itemgetter(1), reverse=True)
    with open(f"{directory}/languages.txt", "w") as f_output:
        for language, counter in s:
            pequal = counter * 100 / processed
            f_output.write(f"{language} - {counter} ({pequal:.2f}%)\n")

    s = "Time used: {0}".format(datetime.datetime.now() - start_time)
    print(s)


def main():
    print("Read data from Wikimedia and extracts the descriptions")

    directory = "extracted/"
    print(f"Output directory: {directory}")
    ensure_dir(directory)
    extract(directory)


if __name__ == "__main__":
    main()
