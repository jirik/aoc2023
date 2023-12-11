from operator import add
from functools import reduce
from itertools import pairwise, permutations, combinations
import re, os, math, sys


def get_dist(ecols, erows, coord1, coord2, size):
    r1, c1 = coord1
    r2, c2 = coord2
    return (abs(r1 - r2) + abs(c1 - c2) +
            sum((size - 1 if rr in erows else 0 for rr in range(min(r1, r2), max(r1, r2)))) +
            sum((size - 1 if cc in ecols else 0 for cc in range(min(c1, c2), max(c1, c2)))))


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = [ln.strip() for ln in f.readlines()]

        space = lines
        ecols = {ci for ci in range(len(space[0])) if all(r[ci] == '.' for r in space)}
        erows = {ri for ri, r in enumerate(space) if r.count('.') == len(r)}
        gs = reduce(add, [[(r, c)] for r, ln in enumerate(space) for c, ch in enumerate(ln) if ch == '#'], [])

        size1 = 2
        r1 = sum([get_dist(ecols, erows, c1, c2, size1) for c1, c2 in combinations(gs, 2)])

        size2 = 1000000
        r2 = sum([get_dist(ecols, erows, c1, c2, size2) for c1, c2 in combinations(gs, 2)])

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
