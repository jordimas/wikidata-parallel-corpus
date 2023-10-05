import sys
import datetime
import zlib

with open("data.1st/en.txt", "r") as f_src, open("data.1st/ca.txt", "r") as f_tgt:
    srcs = {}
    for line in f_src.readlines():
        components = line.split("\t")
        src_id = components[0]
        src_str = components[1]
        srcs[src_id] = src_str

    tgts = {}
    for line in f_tgt.readlines():
        components = line.split("\t")
        tgt_id = components[0]
        tgt_str = components[1]
        tgts[tgt_id] = tgt_str

    already_seen = set()
    with open("en.txt", "w") as f_src, open("ca.txt", "w") as f_tgt:
        total = 0
        written = 0
        for _id, src_str in srcs.items():
            tgt_src = tgts.get(_id)
            if not tgt_src:
                continue

            total += 1
            crc = zlib.crc32(bytes(tgt_src, "utf-8"))
            if crc in already_seen:
                continue

            already_seen.add(crc)
            written += 1
            f_src.write(f"{src_str}\n")
            f_tgt.write(f"{tgt_src}\n")

        print(f"Total: {total}, written: {written}")
