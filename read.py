import ijson
import json
import sys
import datetime
import zlib

items = ijson.items(sys.stdin, 'item', use_float=True)

cnt = 0
export = []
export_all = []

start_time = datetime.datetime.now()
already_seen = set()
with open("output.ca", "w") as f_output_ca, open("output.en", "w") as f_output_en, open("output-debug.txt", "w") as f_output_debug:
    processed = 0 
    for item in items:
        if processed % 1000000 == 0:
            print(f"item processed: {processed}, saved {cnt}, cache {len(already_seen)}")
    
        processed += 1
        
#        print(item)
        new_item = {}
    #    new_item["labels"] = item["labels"]

        descriptions = item.get("descriptions")

        if not descriptions:
            continue

        ca_description = descriptions.get("ca")
        en_description = descriptions.get("en")
        
        if not ca_description or not en_description:
            continue
        
        ca_description = ca_description.get("value")
        en_description = en_description.get("value")
        
        if not ca_description or not en_description:
            continue

        words_en = len(en_description.split())
        words_ca = len(ca_description.split())
        
        MIN_WORDS = 8 # A sentence has average 15-20 words
        if words_en < MIN_WORDS or words_ca < MIN_WORDS:
            continue

        crc = zlib.crc32(bytes(en_description, 'utf-8'))
        if crc in already_seen:
#            print(en_description)
            continue
            
        already_seen.add(crc)            
                                    
#        new_descriptions  = {"ca" : ca_description, "en" : en_description}
#        new_item["descriptions"] =  new_descriptions
         
        if cnt < 5:
#            export.append(new_item)      
            export_all.append(item)
            if cnt == 4:
                with open("output.json", "w") as f_output:
                    json.dump(export_all, f_output, indent = 4, ensure_ascii=False)
            
            
        f_output_en.write(f"{en_description}\n")
        f_output_ca.write(f"{ca_description}\n")

        f_output_debug.write(f"---\n")
        f_output_debug.write(f"{en_description}\n")
        f_output_debug.write(f"{ca_description}\n")
        
        cnt += 1
#        if cnt > 100:        
#            break


    
#with open("output_all.json", "w") as f_output:
#    json.dump(export_all, f_output, indent = 4, ensure_ascii=False) 

s = "Time used: {0}".format(datetime.datetime.now() - start_time)
print(s)    
