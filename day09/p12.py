from functools import reduce
from itertools import pairwise
import re, os, math, sys


def get_values(history):
    seqs = [history]
    while not all(d == 0 for d in seqs[-1]):
        seqs.append([b - a for a, b in pairwise(seqs[-1])])
    return reduce(lambda p, s: s[0] - p, seqs[::-1], 0), reduce(lambda p, s: s[-1] + p, seqs[::-1], 0)


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = [ln.strip() for ln in f.readlines()]

        histories = [[int(v) for v in ln.split(' ')] for ln in lines]

        tuples = [get_values(h) for h in histories]
        p_vals, n_vals = zip(*tuples)
        r1 = sum(n_vals)
        r2 = sum(p_vals)

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
