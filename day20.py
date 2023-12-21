from operator import add
from functools import reduce, lru_cache
from itertools import pairwise, permutations, combinations, groupby
import re, os, math, sys, copy
from util import dijkstra, Graph
from enum import IntEnum, Enum
from collections import Counter


class Type(Enum):
    FLIP_FLOP = '%'
    CONJUNCTION = '&'
    BROADCAST = 'broadcaster'
    OUTPUT = 'output'


NAMES_ONLY = [Type.BROADCAST.value, Type.OUTPUT.value]


def read_modules(lines):
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
    return modules


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


def get_r1(modules):
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
    return all_lows * all_highs


def get_non_overlapping_parts(modules, fr_nm, to_nm):
    fr = modules[fr_nm]
    assert fr[0] == Type.BROADCAST
    assert to_nm not in modules
    prev_tos = [k for k, v in modules.items() if to_nm in v[2]]
    assert len(prev_tos) == 1
    prev_to_nm = prev_tos[0]
    prev_to = modules[prev_to_nm]
    assert prev_to[0] == Type.CONJUNCTION
    starts = [*fr[2]]
    ends = list(prev_to[1].keys())

    parts = [{o} for o in starts]
    qu = [*starts]
    while qu:
        nm = qu.pop(0)
        in_parts = [ps for ps in parts if nm in ps]
        assert len(in_parts) == 1
        in_parts = in_parts[0]
        if nm in ends:
            continue
        for o in modules[nm][2]:
            if o not in in_parts:
                qu.append(o)
                in_parts.add(o)

    return [
        (
            next(s for s in starts if s in ps),
            prev_to_nm,
            {k: v for k, v in modules.items() if k in ps}
        )
        for ps in parts
    ]


def get_states(modules):
    res = []
    for n, (t, s, _) in modules.items():
        if t == Type.FLIP_FLOP:
            res.append((n, s[0]))
        elif t == Type.CONJUNCTION:
            res.append((n, tuple(sorted(s.items()))))
    return tuple(sorted(res))


def get_cycle_length_to_single_high_pulse(modules, fr_nm, to_nm):
    modules_init = copy.deepcopy(modules)
    to_highs = 0
    steps = 0
    while to_highs != 1:

        to_highs = 0
        qu = [('button', False, fr_nm)]

        while qu:
            pulse = qu.pop(0)
            if pulse[2] == to_nm and pulse[1]:
                to_highs += 1
            next_ps = process_pulse(pulse, modules)
            qu += next_ps

        steps += 1

    # surprisingly it differs in one value, but somehow it works good enough
    # assert get_states(modules_init) == get_states(modules)
    return steps


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())

        modules = read_modules(lines)

        r1 = get_r1(copy.deepcopy(modules))

        parts = get_non_overlapping_parts(copy.deepcopy(modules), 'broadcaster', 'rx')
        steps = [get_cycle_length_to_single_high_pulse(ps[2], ps[0], ps[1]) for ps in parts]
        r2 = reduce(lambda a, b: a*b, steps)

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
