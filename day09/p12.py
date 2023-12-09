from functools import reduce
import re, os, math, sys


def get_values(history):
    diffs = [*history]
    seqs = [history]
    while not all(d == 0 for d in seqs[-1]):
        diffs = [
            d - diffs[idx - 1]
            for idx, d in enumerate(diffs)
            if idx > 0
        ]
        seqs.append(diffs)
    return reduce(lambda p, s: s[0] - p, seqs[::-1], 0), reduce(lambda p, s: s[-1] + p, seqs[::-1], 0)


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = [ln.strip() for ln in f.readlines()]

        history = [[int(v) for v in ln.split(' ')] for ln in lines]

        tuples = [get_values(ln) for ln in history]
        p_vals, n_vals = zip(*tuples)
        r1 = sum(n_vals)
        r2 = sum(p_vals)

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
