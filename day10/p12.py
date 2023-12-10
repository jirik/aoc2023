from operator import add
from functools import reduce
import re, os, math, sys

PIPES = {
    'F': {(1, 0), (0, 1)},
    'J': {(-1, 0), (0, -1)},
    '7': {(1, 0), (0, -1)},
    'L': {(-1, 0), (0, 1)},
    '|': {(-1, 0), (1, 0)},
    '-': {(0, -1), (0, 1)},
}


def get_nb_coords(coord):
    r, c = coord
    return {(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)}


def get_linked_pipe_coords(rows, coord):
    return {
        tuple(map(add, coord, d))
        for d in PIPES.get(rows[coord[0]][coord[1]], [])
    }


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            rows = [ln.strip() for ln in f.readlines()]

        s_coord = next(((ri, ci) for ri, ln in enumerate(rows) for ci, c in enumerate(ln) if c == 'S'))

        prev = s_coord
        curr = {
            (r, c) for r, c in get_nb_coords(s_coord)
            if 0 <= r < len(rows) and 0 <= c < len(rows[0])
            and s_coord in get_linked_pipe_coords(rows, (r, c))
        }.pop()
        step = 1
        while rows[curr[0]][curr[1]] != 'S':
            nxt = (get_linked_pipe_coords(rows, curr) - {prev}).pop()
            prev = curr
            curr = nxt
            step += 1

        r1 = step // 2

        print(file_path, r1)


if __name__ == "__main__":
    main()
