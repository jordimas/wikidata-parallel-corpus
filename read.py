import ijson
import json
import sys
import datetime
import zlib
import collections
import operator

items = ijson.items(sys.stdin, "item", use_float=True)

cnt = 0

start_time = datetime.datetime.now()

languages = {}
files = {}
processed = 0
for item in items:
    if processed % 1000000 == 0:
        print(f"item processed: {processed}")

    processed += 1

    new_item = {}

    _id = item.get("id")
    if not _id:
        continue

    descriptions = item.get("descriptions")
    for language in descriptions.keys():
        description = descriptions[language].get("value")
        if len(description) > 0:
            counter = languages.get(language, 0) + 1
            languages[language] = counter
            file_h = files.get(language)
            if not file_h:
                file_h = open(f"data/{language}.txt", "w")
                files[language] = file_h

            file_h.write(f"{_id}\t{description}\n")

    if processed > 1000:
        break

s = sorted(languages.items(), key=operator.itemgetter(1), reverse=True)
with open("languages.txt", "w") as f_output:
    for language, counter in s:
        pequal = counter * 100 / processed
        f_output.write(f"{language} - {counter} ({pequal:.2f}%)\n")

s = "Time used: {0}".format(datetime.datetime.now() - start_time)
print(s)
