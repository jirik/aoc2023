from operator import add
from functools import reduce, lru_cache
from itertools import pairwise, permutations, combinations, groupby
import re, os, math, sys


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = [ln.strip() for ln in f.readlines()]

        r1 = 0

        for ci in range(len(lines[0])):
            stop_idx = -1
            for ri in range(len(lines)):
                c = lines[ri][ci]
                match c:
                    case '.':
                        pass
                    case 'O':
                        stop_idx += 1
                        r1 += len(lines) - stop_idx
                    case '#':
                        stop_idx = ri

        print(file_path, r1)


if __name__ == "__main__":
    main()
