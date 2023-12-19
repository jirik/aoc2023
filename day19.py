from operator import add
from functools import reduce, lru_cache
from itertools import pairwise, permutations, combinations, groupby
import re, os, math, sys
from util import dijkstra, Graph
from enum import IntEnum, Enum


def v_eval(v, expr):
    return eval(expr, locals())


def get_number_of_combinations(cands):
    return reduce(lambda p, c: p*len(c), cands, 1)


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

        rating_names = ['x', 'm', 'a', 's']

        r2 = 0
        wf_cands = {w: [] for w in workflows}
        wf_cands['in'].append(tuple({i for i in range(1, 4001)} for _ in range(4)))
        next_wfs = ['in']
        while next_wfs:
            wf_name = next_wfs.pop(0)
            while wf_cands[wf_name]:
                cands = wf_cands[wf_name].pop(0)
                for expr, next_wf in workflows[wf_name]:
                    rating_idx = next((i for i, r in enumerate(rating_names) if r == expr[0]), None)
                    expr = f"v{expr[1:]}"
                    next_cands = tuple(
                        cs.copy() if cs_idx != rating_idx else {v for v in cs if v_eval(v, expr)}
                        for cs_idx, cs in enumerate(cands)
                    )
                    if next_wf == 'A':
                        r2 += get_number_of_combinations(next_cands)
                    elif next_wf == 'R':
                        pass
                    else:
                        wf_cands[next_wf].append(next_cands)
                        next_wfs.append(next_wf)
                    cands = tuple(
                        cs.copy() if cs_idx != rating_idx else {v for v in cs if v not in next_cands[cs_idx]}
                        for cs_idx, cs in enumerate(cands)
                    )

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
