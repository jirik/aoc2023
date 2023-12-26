import copy
from collections import defaultdict
from operator import add, sub
from functools import reduce, lru_cache
from itertools import pairwise, permutations, combinations, groupby
import re, os, math, sys
from util import dijkstra, Graph
from enum import IntEnum, Enum


def get_dir_char(fr, to):
    dr, dc = tuple(map(sub, to, fr))
    return {
        (1, 0): 'v',
        (-1, 0): '^',
        (0, 1): '>',
        (0, -1): '<',
    }[(dr, dc)]


def read_graph(mp):
    n_rows = len(mp)
    n_cols = len(mp[0])

    s_coord = (0, mp[0].index('.'))
    edges = {}
    qu = {(s_coord, (1, s_coord[1]))}
    e_coord = None
    while qu:
        fr_coord, (r, c) = qu.pop()
        steps = 1
        prev_coord = fr_coord
        while len(next_coords := [(nr, nc) for nr, nc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
                                  if 0 <= nr < n_rows and 0 <= nc < n_cols and prev_coord != (nr, nc)
                                     and mp[nr][nc] != '#']) == 1:
            steps += 1
            next_coord = next_coords[0]
            assert mp[r][c] in ['.', get_dir_char((r, c), next_coord)]
            prev_coord = (r, c)
            r, c = next_coord
        assert all(mp[nr][nc] != '.' for nr, nc in next_coords)
        if not any((r, c) == to for _, to in edges.keys()):
            qu |= {((r, c), (nr, nc)) for (nr, nc) in next_coords if mp[nr][nc] == get_dir_char((r, c), (nr, nc))}
        edges[(fr_coord, (r, c))] = steps
        if not next_coords:
            e_coord = (r, c)
    return edges, s_coord, e_coord


def get_longest_slippery_path(edges, s_coord):
    node_max_steps = {to: None for _, to in edges.keys()}
    node_max_steps[s_coord] = 0
    while (to_node := next((
            to for to, to_max_steps in node_max_steps.items()
            if to_max_steps is None and all(node_max_steps[fr] is not None for fr, to2 in edges.keys() if to == to2)
    ), None)) is not None:
        node_max_steps[to_node] = max(node_max_steps[fr] + steps
                                      for (fr, to), steps in edges.items() if to == to_node)
    return max(node_max_steps.values())


class HashableDict(dict):
    def __hash__(self):
        return 1


@lru_cache(maxsize=None)  # just about 10 seconds faster
def get_longest_path(all_edges, active_edges, fr, e_coord):
    fr_edges = {(f, t) for f, t in active_edges if f == fr or t == fr}
    if fr == e_coord:
        return 0
    if not fr_edges:
        return None
    results = []
    new_active_edges = frozenset(active_edges - fr_edges)
    for fr_edge in fr_edges:
        to = next(c for c in fr_edge if c != fr)
        r = get_longest_path(all_edges, new_active_edges, to, e_coord)
        if r is not None:
            results.append(r + all_edges[fr_edge])
    result = max(results) if results else None
    return result


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())
        mp = lines

        edges, s_coord, e_coord = read_graph(mp)

        r1 = get_longest_slippery_path(edges, s_coord)

        r2 = get_longest_path(HashableDict(edges.items()), frozenset(edges.keys()), s_coord, e_coord)

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
