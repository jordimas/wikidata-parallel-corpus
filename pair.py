import sys
import datetime
import zlib
import datetime


def _is_sentence_len_good(src, trg):
    src = src.strip()
    trg = trg.strip()
    lsrc = len(src)
    ltrg = len(trg)

    if lsrc == 0 or ltrg == 0:
        return False

    MIN_CHARS = 40
    if max(lsrc, ltrg) > MIN_CHARS:
        size_diff_percentage = 70
        if lsrc < ltrg:
            tmp = lsrc
            lsrc = ltrg
            ltrg = tmp

        # 20-10
        diff = (lsrc - ltrg) / lsrc * 100

        cnd = diff > size_diff_percentage
        #
        if cnd:
            return False

        print(f"{diff} - {cnd} - {src} - {trg}")

    return True


# _is_sentence_len_good(" Estonian teacher and local historian, worked in Kihnu", " Estonian teacher Estonian teacher  Estonian teacher")
# exit(0)

with open("data.1st/en.txt", "r") as f_src, open("data.1st/ca.txt", "r") as f_tgt, open(
    "pair-debug.txt", "w"
) as f_output_debug:
    start_time = datetime.datetime.now()

    srcs = {}
    for line in f_src.readlines():
        components = line.split("\t")
        src_id = components[0]
        src_str = components[1].rstrip()
        srcs[src_id] = src_str

    tgts = {}
    for line in f_tgt.readlines():
        components = line.split("\t")
        tgt_id = components[0]
        tgt_str = components[1].rstrip()
        tgts[tgt_id] = tgt_str

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

            #            if not _is_sentence_len_good(src_str, tgt_str):
            #                print(f"{src_str}")
            #                print(f"{tgt_str}\n")
            #                diff += 1
            #                continue

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
