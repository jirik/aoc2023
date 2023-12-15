from operator import add
from functools import reduce, lru_cache
from itertools import pairwise, permutations, combinations, groupby
import re, os, math, sys


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())

        ln = lines[0]
        r1 = sum(reduce(lambda p, c: (p+ord(c))*17 % 256, st, 0) for st in ln.split(','))

        print(file_path, r1)


if __name__ == "__main__":
    main()
