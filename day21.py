import copy
from operator import add
from functools import reduce, lru_cache
from itertools import pairwise, permutations, combinations, groupby
import re, os, math, sys
from util import dijkstra, Graph
from enum import IntEnum, Enum


def get_nbs(coord):
    r, c = coord
    return {(r + 1, c), (r - 1, c), (r, c - 1), (r, c + 1)}


def get_steps_from_coord(mp, start_coord):
    coords = set()
    hist = []
    curr_coords = {start_coord}
    while diff := curr_coords - coords:
        hist.append(diff)
        coords |= diff
        curr_coords = reduce(lambda p, coord: p | {
            (r, c) for r, c in get_nbs(coord) if 0 <= r < len(mp) and 0 <= c < len(mp[0]) and mp[r][c] != '#'
        }, diff, set())
    return hist


def get_steps_from_nine_coords(mp):
    result = {}
    for r in [0, len(mp) // 2, len(mp) - 1]:
        for c in [0, len(mp) // 2, len(mp) - 1]:
            steps_hist = get_steps_from_coord(copy.deepcopy(mp), (r, c))
            result[(r, c)] = steps_hist
            exp_steps = max(abs(r - 0), abs(r - (len(mp) - 1))) + max(abs(c - 0), abs(c - (len(mp[0]) - 1)))
            if len(mp) > 11:
                assert len(steps_hist) - 1 == exp_steps  # relevant for real input only
    return result


def get_n_odds_evens(steps_hist):
    odds = sum(len(cs) for csi, cs in enumerate(steps_hist) if (csi + 1) % 2 == 1)
    evens = sum(len(cs) for cs in steps_hist) - odds
    return odds, evens


def get_n_steps(steps_hist):
    mod = len(steps_hist) % 2
    return sum(len(cs) for csi, cs in enumerate(steps_hist) if (csi + 1) % 2 == mod)


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())

        mp = lines

        s_coord = next((ri, r.index('S')) for ri, r in enumerate(mp) if 'S' in r)
        steps = 6 if len(mp) == 11 else 64
        steps_from_nine_coords = get_steps_from_nine_coords(mp)
        r1 = get_n_steps(steps_from_nine_coords[s_coord][1:steps+1]) + 1
        r2 = None

        if len(mp) > 11:

            tile_size = len(mp)
            tile_half = tile_size // 2

            STEPS = 26501365

            assert all(all(c in ['.', 'S'] for c in mp[ri]) for ri in [0, tile_half, tile_size-1])
            assert all(all(r[ci] in ['.', 'S'] for r in mp) for ci in [0, tile_half, tile_size-1])

            bg_full_buffer = (STEPS - tile_half * 2) // tile_size
            orthog_border_full_tile_is_start_color = bg_full_buffer % 2 == 0

            assert orthog_border_full_tile_is_start_color is False

            missing_orthog_steps = STEPS - tile_half - bg_full_buffer * tile_size
            assert tile_half < missing_orthog_steps <= tile_size
            missing_outer_diag_steps = missing_orthog_steps - tile_half - 1
            missing_inner_diag_steps = missing_outer_diag_steps + tile_size

            n_full_start_tiles = bg_full_buffer * bg_full_buffer
            n_full_other_tiles = (bg_full_buffer + 1) * (bg_full_buffer + 1)

            n_outer_diag_tiles = bg_full_buffer + 1
            n_inner_diag_tiles = bg_full_buffer

            assert STEPS % 2 == 1  # start tile contains odds
            steps_from_center_without_s = steps_from_nine_coords[s_coord][1:]
            n_steps_in_full_start_tile, n_steps_in_full_other_tile = get_n_odds_evens(steps_from_center_without_s)
            n_steps_in_full_other_tile += 1  # for S

            n_steps_orthog_border_tiles = sum(
                get_n_steps(steps_from_nine_coords[coord][:missing_orthog_steps])
                for coord in [(tile_half, 0), (0, tile_half), (tile_size - 1, tile_half), (tile_half, tile_size - 1)]
            )

            n_steps_diag_border_tiles = sum(
                get_n_steps(steps_from_nine_coords[coord][:missing_outer_diag_steps]) * n_outer_diag_tiles
                + get_n_steps(steps_from_nine_coords[coord][:missing_inner_diag_steps]) * n_inner_diag_tiles
                for coord in [(0, 0), (0, tile_size - 1), (tile_size - 1, 0), (tile_size - 1, tile_size - 1)]
            )

            r2 = (n_full_start_tiles * n_steps_in_full_start_tile
                  + n_full_other_tiles * n_steps_in_full_other_tile
                  + n_steps_orthog_border_tiles + n_steps_diag_border_tiles)

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
