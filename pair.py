import sys
import datetime
import zlib
import datetime
import logging
import os

logging.basicConfig(filename="pair.log", encoding="utf-8", level=logging.DEBUG)

MAX_DIFF_PERCENTAGE = 40

import re
def has_numbers(inputString):
    return bool(re.search(r'\d', inputString))

def _is_sentence_len_good(src, trg):
    src = src.strip()
    trg = trg.strip()
    lsrc = len(src)
    ltrg = len(trg)

    if lsrc == 0 or ltrg == 0:
        return False

    # The lower the better
    size_diff_percentage = MAX_DIFF_PERCENTAGE
    if lsrc < ltrg:
        tmp = lsrc
        lsrc = ltrg
        ltrg = tmp

    diff = (lsrc - ltrg) / lsrc * 100
    cnd = diff < size_diff_percentage
    #       print(f"{diff} - {cnd} - {src} - {trg}")

 #   print(f"{diff} - {cnd} - {lsrc} - {ltrg} - {src} - {trg}")
    return cnd


# _is_sentence_len_good("conflicte bèl·lic global que tingué lloc entre els anys 1939 i 1945", "global war, 1939 global war")
#_is_sentence_len_good("person(s) who wrote the m   usic [for lyricist, use lyrics by (P676)]", "autor de la música autor ")
#exit(0)

MIN_WORDS = 2

def _min_len(src, trg):
    words_src = src.split()
    words_trg = trg.split()
    return len(words_src) > MIN_WORDS and len(words_trg) > MIN_WORDS


def _load_string_for_language(language):
    part = 1
    strings = {}
    while True:
        filename = f"data/{language}-{part}.txt"
        if not os.path.exists(filename):
            break

        with open(filename) as f_tgt:
            for line in f_tgt.readlines():
                components = line.split("\t")
                tgt_id = components[0]
                tgt_str = components[1].rstrip()
                strings[tgt_id] = tgt_str

            part += 1

    print(f"Read language {language} with {part} parts and {len(strings)} lines")
    return strings


with open("en.txt", "w") as f_src, open("ca.txt", "w") as f_tgt, open("pair-debug.txt", "w") as f_output_debug:
    start_time = datetime.datetime.now()

    srcs = _load_string_for_language("en")
    tgts = _load_string_for_language("ca")
    already_seen = set()
    total = 0
    written = 0
    diff = 0
    duplicated = 0    
    too_small = 0
    for _id, src_str in srcs.items():
        total += 1
        tgt_str = tgts.get(_id)
        if not tgt_str:
            continue
            
        if has_numbers(src_str) or has_numbers(tgt_str):
            continue

        if not _min_len(src_str, tgt_str):
            too_small += 1
            continue

        if not _is_sentence_len_good(src_str, tgt_str):
            diff += 1
            continue

        crc = zlib.crc32(bytes(src_str, "utf-8"))
        if crc in already_seen:
            duplicated += 1
            continue

        already_seen.add(crc)
        written += 1
        f_src.write(f"{src_str}\n")
        f_tgt.write(f"{tgt_str}\n")

        f_output_debug.write(f"---\n")
        f_output_debug.write(f"{src_str}\n")
        f_output_debug.write(f"{tgt_str}\n")

    print(
        f"Total: {total}, too small {too_small}, diff discarted {diff}, duplicated {duplicated}, written: {written} - diff percentage {MAX_DIFF_PERCENTAGE}"
    )
    print("Time used: {0}".format(datetime.datetime.now() - start_time))
