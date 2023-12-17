from operator import add
from functools import reduce, lru_cache
from itertools import pairwise, permutations, combinations, groupby
import re, os, math, sys
from util import dijkstra, Graph


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())
        mp = [[int(c) for c in ln] for ln in lines]

        n_rows = len(mp)
        n_cols = len(mp[0])
        max_steps = 3
        edges = set()
        for ri, r in enumerate(mp):
            for ci, c in enumerate(r):
                curr_edges = [
                    ((ri, ci, '|'), (ri, ic, '-'), sum(r[ic:ci]))
                    for ic in range(max(0, ci - max_steps), ci)
                ] + [
                    ((ri, ci, '|'), (ri, ic, '-'), sum(r[ci+1:ic+1]))
                    for ic in range(ci + 1, min(n_cols, ci + max_steps + 1))
                ] + [
                    ((ri, ci, '-'), (ir, ci, '|'), sum(ir2[ci] for ir2 in mp[ir:ri]))
                    for ir in range(max(0, ri - max_steps), ri)
                ] + [
                    ((ri, ci, '-'), (ir, ci, '|'), sum(ir2[ci] for ir2 in mp[ri+1:ir+1]))
                    for ir in range(ri + 1, min(n_rows, ri + max_steps + 1))
                ]
                edges |= set(curr_edges)

        graph = Graph()
        for e in edges:
            graph.add_edge(*e)

        start_n = (-1, -1, 's')
        graph.add_edge(start_n, (0, 0, '-'), 0)
        graph.add_edge(start_n, (0, 0, '|'), 0)

        end_nodes = {(n_rows-1, n_cols-1, '-'), (n_rows-1, n_cols-1, '|')}

        pth = dijkstra(graph, start_n, end_nodes)

        r1 = sum(graph.weights[e] for e in pairwise(pth))

        print(file_path, r1)


if __name__ == "__main__":
    main()
