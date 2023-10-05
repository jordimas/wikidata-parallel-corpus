import ijson
import json
import sys
import datetime
import zlib
import collections
import operator

with open("data.1st/en.txt", "r") as f_src, open("data.1st/ca.txt", "r") as f_tgt:
    srcs = {}
    for line in f_src.readlines()[0:500000]:
        components = line.split("\t")
        src_id = components[0]
        src_str = components[1]
        srcs[src_id] = src_str

    tgts = {}
    for line in f_tgt.readlines()[0:500000]:
        components = line.split("\t")
        tgt_id = components[0]
        tgt_str = components[1]
        tgts[src_id] = tgt_str

    with open("en.txt", "w") as f_src, open("ca.txt", "w") as f_tgt:
        for _id, src_str in srcs.items():
            tgt_src = tgts.get(_id)
            if not tgt_src:
                continue
                
            f_src.write(f"{src_str}\n")
            f_tgt.write(f"{tgt_src}\n")
