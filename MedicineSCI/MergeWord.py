#-*- coding:utf-8 -*-
import os
import argparse
import re

from collections import defaultdict
###

###

def main(args):
    table = args.table
    folder = args.dir
    files = os.listdir(folder)

    d = defaultdict(str)
    with open(table) as r:
        value = None
        for l in r:
            l = l.strip()
            if value == None:
                if l.startswith("**"):
                    value = l[2:]
                else:
                    pass
            else:
                if l.startswith("**"):
                    value = l[2:]
                elif l:
                    key = l.split(" ", 2)[2]
                    key = key[1:len(key) - 1]
                    d[key] = value

    for f in files:
        f = folder+"\\"+f
        with open(f,"r") as r, open("%s.out" % f,"a") as w:
            for l in r:
                l = l.strip()
                out = l
                if l in d:
                    out = d[l]
                w.write("%s\n" % out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--table", required=True)
    parser.add_argument("--dir", required=True)
    args = parser.parse_args()
    main(args)
