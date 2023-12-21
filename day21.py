from operator import add
from functools import reduce, lru_cache
from itertools import pairwise, permutations, combinations, groupby
import re, os, math, sys
from util import dijkstra, Graph
from enum import IntEnum, Enum


def get_nbs(coord):
    r, c = coord
    return {(r+1, c), (r-1, c), (r, c-1), (r, c+1)}


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())
        mp = lines

        s_coord = next((ri, r.index('S')) for ri, r in enumerate(mp) if 'S' in r)
        steps = 6 if len(mp) == 11 else 64
        coords = {s_coord}
        for _ in range(steps):
            coords = reduce(lambda p, coord: p | {
                (r, c) for r, c in get_nbs(coord) if 0 <= r < len(mp) and 0 <= c < len(mp[0]) and mp[r][c] != '#'
            }, coords, set())

        r1 = len(coords)

        print(file_path, r1)


if __name__ == "__main__":
    main()
