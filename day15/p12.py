from operator import add
from functools import reduce, lru_cache
from itertools import pairwise, permutations, combinations, groupby
import re, os, math, sys


def hash_str(s):
    return reduce(lambda p, c: (p+ord(c))*17 % 256, s, 0)


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())

        ln = lines[0]
        r1 = sum(hash_str(s) for s in ln.split(','))

        boxes = [[] for _ in range(256)]
        for sti, st in enumerate(ln.split(',')):
            lbl, op, foc_l = re.match(r'^([^-=]+)([-=])(\d*)$', st).groups()
            bxi = hash_str(lbl)
            bx = boxes[bxi]
            lsi = next((i for i in range(len(bx)) if bx[i][0] == lbl), None)
            if op == '=':
                if lsi is not None:
                    bx[lsi] = (lbl, foc_l)
                else:
                    bx.append((lbl, foc_l))
            else:
                if lsi is not None:
                    del bx[lsi]

        r2 = sum((bi+1)*(li+1)*int(fl) for bi, bx in enumerate(boxes) for li, (_, fl) in enumerate(bx))

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
