from functools import reduce
import re, os, math, sys


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = [ln.strip() for ln in f.readlines()]

        seq = lines[0]
        tuples = [
            (ln[0:3], ln[7:10], ln[12:15])
            for ln in lines[2:]
        ]
        lmap, rmap = reduce(lambda pr, t: (pr[0] | {t[0]: t[1]}, pr[1] | {t[0]: t[2]}), tuples, ({}, {}))

        cnode = 'AAA'
        step = 0
        while 'ZZZ' != cnode:
            move = seq[step % len(seq)]
            mp = lmap if move == 'L' else rmap
            cnode = mp[cnode]
            step += 1

        r1 = step

        print(file_path, r1)


if __name__ == "__main__":
    main()
