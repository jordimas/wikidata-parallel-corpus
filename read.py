import ijson
import json
import sys
import datetime
import zlib
import collections
import operator

items = ijson.items(sys.stdin, 'item', use_float=True)

cnt = 0
export = []
export_all = []

start_time = datetime.datetime.now()
already_seen = set()

languages = {}
with open("output.ca", "w") as f_output_ca, open("output.en", "w") as f_output_en, open("output-debug.txt", "w") as f_output_debug:
    processed = 0 
    for item in items:
        if processed % 1000000 == 0:
            print(f"item processed: {processed}")
    
        processed += 1
        
        new_item = {}

        descriptions = item.get("descriptions")
        for language in descriptions.keys():
            description = descriptions[language].get("value")
#            print(f"{language} - {description}")
            if len(description) > 0:
                counter = languages.get(language, 0) + 1
                languages[language] = counter
 
            
        if processed > 5000000:
            break

s = sorted(languages.items(), key=operator.itemgetter(1), reverse=True)
for language, counter in s:
    pequal = counter * 100 / processed
    print(f"{language} - {counter} ({pequal:.2f}%)")
    
#with open("output_all.json", "w") as f_output:
#    json.dump(export_all, f_output, indent = 4, ensure_ascii=False) 

s = "Time used: {0}".format(datetime.datetime.now() - start_time)
print(s)    
