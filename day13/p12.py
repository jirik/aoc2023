from operator import add
from functools import reduce, lru_cache
from itertools import pairwise, permutations, combinations, groupby
import re, os, math, sys


def get_refls(note):
    res = 0
    len_r = len(note[0])
    for ci in range(1, len_r//2 + 1):
        if all(r[0:ci] == r[ci:ci*2][::-1] for r in note):
            res += ci
        if all(r[len_r - ci:len_r] == r[len_r - ci * 2:len_r - ci][::-1] for r in note):
            res += len_r-ci
    return res


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = [ln.strip() for ln in f.readlines()]

        notes = [list(g) for k, g in groupby(lines, key=lambda ln: bool(ln)) if k]

        r1 = sum([get_refls(n) + 100 * get_refls([''.join(t) for t in zip(*n)]) for n in notes])

        print(file_path, r1)


if __name__ == "__main__":
    main()
