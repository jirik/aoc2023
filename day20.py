from operator import add
from functools import reduce, lru_cache
from itertools import pairwise, permutations, combinations, groupby
import re, os, math, sys
from util import dijkstra, Graph
from enum import IntEnum, Enum
from collections import Counter


class Type(Enum):
    FLIP_FLOP = '%'
    CONJUNCTION = '&'
    BROADCAST = 'broadcaster'
    OUTPUT = 'output'


NAMES_ONLY = [Type.BROADCAST.value, Type.OUTPUT.value]


def process_pulse(pulse, modules):
    fr, p, to = pulse
    if to not in modules:
        return []
    tp, state, outputs = modules[to]
    rp = None
    if tp == Type.FLIP_FLOP and not p:
        rp = not state[0]
        state[0] = not state[0]
    elif tp == Type.CONJUNCTION:
        state[fr] = p
        rp = not all(state.values())
    elif tp == Type.BROADCAST:
        rp = p
    res = [] if rp is None else [(to, rp, o) for o in outputs]
    return res


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())

        raw_modules = {}
        for ln in lines:
            left_s, right_s = ln.split(' -> ')
            if left_s in NAMES_ONLY:
                nm = left_s
                tp = Type(left_s)
            else:
                nm = left_s[1:]
                tp = Type(left_s[0])
            outputs = right_s.split(', ')
            raw_modules[nm] = (tp, outputs)

        modules = {}
        for nm, (tp, outputs) in raw_modules.items():
            state = None
            if tp == Type.FLIP_FLOP:
                state = [False]
            elif tp == Type.CONJUNCTION:
                state = {
                    n: False
                    for n, (_, outs) in raw_modules.items() if nm in outs
                }
            modules[nm] = (tp, state, outputs)

        all_lows = 0
        all_highs = 0

        steps = 1000
        while steps > 0:

            lows = 1
            highs = 0
            qu = [('button', False, 'broadcaster')]

            while qu:
                pulse = qu.pop(0)
                next_ps = process_pulse(pulse, modules)
                hs = sum(p for _, p, _ in next_ps if p)
                ls = len(next_ps) - hs
                lows += ls
                highs += hs
                qu += next_ps

            all_lows += lows
            all_highs += highs
            steps -= 1

        r1 = all_lows * all_highs

        print(file_path, r1)


if __name__ == "__main__":
    main()
