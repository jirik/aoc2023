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


def get_area(pth, rows):
    rs, cs = zip(*pth)
    a = 0
    for r in range(min(*rs), max(rs) + 1):
        inside = False
        from_v_dir = 0
        for c in range(min(*cs), max(cs) + 1):
            coord_in_path = (r, c) in pth
            if coord_in_path:
                v_dirs = [c[0] for c in PIPES[rows[r][c]] if c[0]]
                if len(v_dirs) == 2:
                    inside = not inside
                elif len(v_dirs) == 1:
                    if from_v_dir == 0:
                        from_v_dir = v_dirs[0]
                    elif from_v_dir == v_dirs[0]:
                        from_v_dir = 0
                    else:
                        inside = not inside
                        from_v_dir = 0
            elif inside:
                a += 1
    return a


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            rows = [ln.strip() for ln in f.readlines()]

        s_coord = next(((ri, ci) for ri, ln in enumerate(rows) for ci, c in enumerate(ln) if c == 'S'))

        curr = {
            (r, c) for r, c in get_nb_coords(s_coord)
            if 0 <= r < len(rows) and 0 <= c < len(rows[0])
            and s_coord in get_linked_pipe_coords(rows, (r, c))
        }.pop()
        pth = [s_coord]
        while rows[curr[0]][curr[1]] != 'S':
            pth.append(curr)
            curr = (get_linked_pipe_coords(rows, curr) - {pth[-2]}).pop()

        r1 = len(pth) // 2

        s_shape = next((
            k for k, v in PIPES.items()
            if tuple(map(lambda s, n: n - s, s_coord, pth[1])) in v
            and tuple(map(lambda s, p: p - s, s_coord, pth[-1])) in v
        ))
        rows = [r.replace('S', s_shape) for r in rows]

        r2 = get_area(pth, rows)
        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
