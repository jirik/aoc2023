import copy
from operator import add
from functools import reduce, lru_cache
from itertools import pairwise, permutations, combinations, groupby
import re, os, math, sys
from util import dijkstra, Graph
from enum import IntEnum, Enum


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())

        bricks = [
            tuple(tuple(int(c)for c in part.split(',')) for part in ln.split('~'))
            for ln in lines
        ]
        bricks.sort(key=lambda b: b[0][2])

        for (x1, y1, z1), (x2, y2, z2) in bricks:
            assert x1 <= x2 and y1 <= y2 and z1 <= z2

        x_size = max(b[1][0] for b in bricks) + 1
        y_size = max(b[1][1] for b in bricks) + 1
        wall_top = [[(0, None)] * y_size for _ in range(x_size)]  # height, brick_index

        upper_lowers = {}
        lower_uppers = {i: set() for i in range(len(bricks))}

        for bri, ((x1, y1, z1), (x2, y2, z2)) in enumerate(bricks):
            brs_under = {wall_top[x][y] for x in range(x1, x2+1) for y in range(y1, y2+1)}
            max_h = max(t[0] for t in brs_under)
            touched_brs_under = {t[1] for t in brs_under if t[0] == max_h if t[1] is not None}
            upper_lowers[bri] = touched_brs_under
            for b_under in touched_brs_under:
                lower_uppers[b_under].add(bri)
            new_top = max_h + (z2 - z1 + 1)
            for x in range(x1, x2 + 1):
                for y in range(y1, y2+1):
                    wall_top[x][y] = (new_top, bri)

        r1 = sum(all(len(upper_lowers[u]) > 1 for u in lower_uppers[b]) for b in range(len(bricks)))

        print(file_path, r1)


if __name__ == "__main__":
    main()
