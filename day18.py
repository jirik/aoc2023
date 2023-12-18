from operator import add
from functools import reduce, lru_cache
from itertools import pairwise, permutations, combinations, groupby
import re, os, math, sys
from util import dijkstra, Graph
from enum import IntEnum, Enum


class Dir(Enum):
    R = 'R'
    D = 'D'
    L = 'L'
    U = 'U'


def add_dir(row, col, direction, length):
    if direction == Dir.U:
        return row-length, col
    elif direction == Dir.D:
        return row+length, col
    elif direction == Dir.L:
        return row, col-length
    elif direction == Dir.R:
        return row, col+length
    else:
        raise 'oops'


def get_area(plan):
    area = 0
    border = 0
    coord = (0, 0)
    for drc, lng in plan:
        r, c = coord
        next_coord = add_dir(*coord, drc, lng)
        nr, nc = next_coord
        area += (r + nr) * (c - nc) / 2
        border += abs(c - nc) if r == nr else abs(r - nr)
        coord = next_coord
    return round(area + border//2 + 1)


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())

        plan = [(Dir(parts[0]), int(parts[1])) for ln in lines if (parts := ln.split(' '))]

        r1 = get_area(plan)

        dir_list = [e for e in Dir]
        plan2 = [(dir_list[int(p[7])], int(p[2:7], 16)) for ln in lines if (p := ln.split(' ')[-1])]
        r2 = get_area(plan2)

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
