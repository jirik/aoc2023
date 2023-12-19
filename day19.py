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

        workflows, ratings = [list(g) for k, g in groupby(lines, key=lambda ln: bool(ln)) if k]
        workflows = {
            m.group(1): [
                (('True' if len(parts) == 1 else parts[0]), parts[-1])
                for rule in m.group(2).split(',')
                if (parts := rule.split(':'))
            ]
            for w in workflows
            if (m := re.match(r'^(\w+)\{(.+)}$', w))
        }
        ratings = [
            {
                parts[0]: int(parts[1])
                for stmt in rating[1:-1].split(',')
                if (parts := stmt.split('='))
            }
            for rating in ratings
        ]

        r1 = 0
        for rating in ratings:
            x = rating['x']
            m = rating['m']
            a = rating['a']
            s = rating['s']
            scope = locals()
            wf_name = 'in'
            while wf_name not in {'A', 'R'}:
                rules = workflows[wf_name]
                wf_name = next(wf_name for expr, wf_name in rules if eval(expr, scope))
            if wf_name == 'A':
                r1 += x + m + a + s

        print(file_path, r1)


if __name__ == "__main__":
    main()
