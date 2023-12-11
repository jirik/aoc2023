from operator import add
from functools import reduce
from itertools import pairwise, permutations, combinations
import re, os, math, sys


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = [ln.strip() for ln in f.readlines()]

        space_v = reduce(lambda p, ln: p + ([ln]*(2 if ln.count('.') == len(ln) else 1)), lines, [])
        ncols = len(space_v[0])
        space = [
            ''.join(reversed([ln[ci]*(2 if all(l2[ci] == '.' for l2 in space_v) else 1) for ci in range(ncols-1, -1, -1)]))
            for ln in space_v
        ]

        gs = reduce(add, [[(r, c)] for r, ln in enumerate(space) for c, ch in enumerate(ln) if ch == '#'], [])

        r1 = sum([abs(r1-r2) + abs(c1-c2) for (r1, c1), (r2, c2) in combinations(gs, 2)])
        print(file_path, r1)


if __name__ == "__main__":
    main()
