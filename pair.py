import sys
import datetime
import zlib
import datetime
import logging

logging.basicConfig(filename='pair.log', encoding='utf-8', level=logging.DEBUG)

def _is_sentence_len_good(src, trg):
    src = src.strip()
    trg = trg.strip()
    lsrc = len(src)
    ltrg = len(trg)

    if lsrc == 0 or ltrg == 0:
        return False

#    MIN_CHARS = 15
#    if max(lsrc, ltrg) > MIN_CHARS:
 
    # the lower % better
    size_diff_percentage = 30
    if lsrc < ltrg:
        tmp = lsrc
        lsrc = ltrg
        ltrg = tmp

    diff = (lsrc - ltrg) / lsrc * 100
    cnd = diff > size_diff_percentage
#       print(f"{diff} - {cnd} - {src} - {trg}")

    logging.debug(f"{diff} - {cnd} - {lsrc} - {ltrg} - {src} - {trg}")
    return cnd


#_is_sentence_len_good("conflicte bèl·lic global que tingué lloc entre els anys 1939 i 1945", "global war, 1939 global war")
#_is_sentence_len_good("spread made from fruit", "gel")
#exit(0)

with open("data.1st/en.txt", "r") as f_src, open("data.1st/ca.txt", "r") as f_tgt, open(
    "pair-debug.txt", "w"
) as f_output_debug:
    start_time = datetime.datetime.now()

    tgts = {}
    for line in f_tgt.readlines()[0:100000]:
        components = line.split("\t")
        tgt_id = components[0]
        tgt_str = components[1].rstrip()
        tgts[tgt_id] = tgt_str    

    srcs = {}
    for line in f_src.readlines()[0:100000]:
        components = line.split("\t")
        src_id = components[0]
        src_str = components[1].rstrip()
        if src_id in tgts:
            srcs[src_id] = src_str

    already_seen = set()
    with open("en.txt", "w") as f_src, open("ca.txt", "w") as f_tgt:
        total = 0
        written = 0
        diff = 0
        duplicated = 0
        for _id, src_str in srcs.items():
            tgt_src = tgts.get(_id)
            if not tgt_src:
                continue

            if not _is_sentence_len_good(src_str, tgt_str):
                diff += 1
                continue

            total += 1
            crc = zlib.crc32(bytes(src_str, "utf-8"))
            if crc in already_seen:
                duplicated += 1
                continue

            already_seen.add(crc)
            written += 1
            f_src.write(f"{src_str}\n")
            f_tgt.write(f"{tgt_src}\n")

            f_output_debug.write(f"---\n")
            f_output_debug.write(f"{src_str}\n")
            f_output_debug.write(f"{tgt_src}\n")

        print(
            f"Total: {total}, diff discarted {diff}, duplicated {duplicated}, written: {written}"
        )
        print("Time used: {0}".format(datetime.datetime.now() - start_time))
