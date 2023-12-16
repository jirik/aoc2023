from operator import add
from functools import reduce, lru_cache
from itertools import pairwise, permutations, combinations, groupby
import re, os, math, sys

L = '<'
R = '>'
D = 'v'
U = '^'

HDIRS = [L, R]
VDIRS = [U, D]

SLASH_MAP = {
    R: U,
    U: R,
    L: D,
    D: L,
}
BACKSLASH_MAP = {
    R: D,
    D: R,
    U: L,
    L: U,
}


def shift(prow, pcol, pdir):
    r = prow
    c = pcol
    if pdir == L:
        c -= 1
    elif pdir == R:
        c += 1
    elif pdir == D:
        r += 1
    elif pdir == U:
        r -= 1
    return r, c


def energize(space, checked, prev_tuple):
    qu = [prev_tuple]

    while qu:
        pr, pc, pdir = qu.pop(0)
        ri, ci = shift(pr, pc, pdir)
        if not (0 <= ri < len(space) and 0 <= ci < len(space)):
            continue

        coord = (ri, ci)
        if coord not in checked:
            checked[coord] = []
        if pdir in checked[coord]:
            continue
        else:
            checked[coord].append(pdir)

        c = space[ri][ci]
        if c == '.':
            qu.append((ri, ci, pdir))
        elif c == '-' and pdir in HDIRS or c == '|' and pdir in VDIRS:
            qu.append((ri, ci, pdir))
        elif c == '-':
            qu += [(ri, ci, d) for d in HDIRS]
        elif c == '|':
            qu += [(ri, ci, d) for d in VDIRS]
        elif c == '/':
            qu.append((ri, ci, SLASH_MAP[pdir]))
        elif c == '\\':
            qu.append((ri, ci, BACKSLASH_MAP[pdir]))

    return checked


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())
        space = lines

        checked = {}

        energize(space, checked, (0, -1, R))
        r1 = len(checked)

        results = []
        for ri in range(len(space)):
            results.append(energize(space, {}, (ri, -1, R)))
            results.append(energize(space, {}, (ri, len(space[0]), L)))
        for ci in range(len(space[0])):
            results.append(energize(space, {}, (-1, ci, D)))
            results.append(energize(space, {}, (len(space), ci, U)))
        r2 = max([len(c) for c in results])

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
