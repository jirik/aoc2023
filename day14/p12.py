from operator import add
from functools import reduce, lru_cache
from itertools import pairwise, permutations, combinations, groupby
import re, os, math, sys


def tilt_north(rows):
    cols = []
    for ci in range(len(rows[0])):
        stop_idx = -1
        col = []
        for ri in range(len(rows)):
            c = rows[ri][ci]
            match c:
                case '.':
                    col += [c]
                case 'O':
                    col += ['.']
                    stop_idx += 1
                    col[stop_idx] = 'O'
                case '#':
                    col += [c]
                    stop_idx = ri
        cols.append(col)
    return tuple(''.join(c) for c in cols)


def get_west_load(rows):
    len_r = len(rows[0])
    return sum(len_r - ci for r in rows for ci, c in enumerate(r) if c == 'O')


def get_north_load(rows):
    n_rows = len(rows)
    return sum(n_rows - ri for ri, r in enumerate(rows) for c in r if c == 'O')


def cycle(rows):
    for _ in range(2):
        rows = tilt_north(rows)
        rows = tilt_north(rows)
        rows = tuple(r[::-1] for r in rows[::-1])
    return rows


def print_rows(rows):
    for r in rows:
        print(r)
    print()


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())

        r1 = get_west_load(tilt_north(lines))

        rows = lines
        cache = {rows: 0}
        cyc_i = 0
        while (rows := cycle(rows)) not in cache:
            cyc_i += 1
            cache[rows] = cyc_i
        start_idx = cache[rows]

        CYCLES = 1000000000

        remaining_cycles = (CYCLES - start_idx) % (cyc_i+1 - start_idx)

        for _ in range(remaining_cycles):
            rows = cycle(rows)

        r2 = get_north_load(rows)

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
