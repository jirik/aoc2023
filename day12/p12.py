from operator import add
from functools import reduce, lru_cache
from itertools import pairwise, permutations, combinations
import re, os, math, sys


@lru_cache(maxsize=None)
def get_broken_positions(seq, br):
    return [
        i
        for i in range(len(seq) - br + 1)
        if seq[i:i+br].count('.') == 0 and (i == 0 or seq[i-1] != '#') and (i + br == len(seq) or seq[i+br] != '#')
    ]


@lru_cache(maxsize=None)
def get_partitions(parts):
    result = 1
    for pidx, (seq, brokens) in enumerate(parts):
        n_br = len(brokens)
        len_seq = len(seq)
        if n_br == 0:
            result *= int('#' not in seq)
            continue
        if len_seq == 0:
            result *= int(n_br == 0)
            continue

        # just little speed-up
        cross_cnt = seq.count('#')
        sum_br = sum(brokens)
        if cross_cnt > sum_br or cross_cnt + seq.count('?') < sum_br:
            result *= 0
            continue

        max_br = max(brokens)
        br_idx = next((i for i in range(n_br) if brokens[i] == max_br))
        br = brokens[br_idx]
        r = 0
        for pos in get_broken_positions(seq, br):
            r += get_partitions((
                (seq[:max(0, pos - 1)], brokens[:br_idx]),
                (seq[min(len_seq, pos + br + 1):], brokens[br_idx + 1:]),
            ))
        result *= r
    return result


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = [ln.strip() for ln in f.readlines()]

        tuples = [(p[0], tuple(int(c) for c in p[1].split(','))) for ln in lines if (p := ln.split(' '))]
        r1 = sum([get_partitions(((seq, brokens),)) for seq, brokens in tuples])

        # r2 = 0
        # for idx, (s, b) in enumerate(tuples):
        #     r2 += get_partitions((('?'.join([s]*5), b*5),))
        #     print('ln', idx)

        r2 = sum([get_partitions((('?'.join([s]*5), b*5),)) for s, b in tuples])

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
