from operator import add
from functools import reduce, lru_cache
from itertools import pairwise, permutations, combinations, groupby
import re, os, math, sys


def get_refls(note):
    res = set()
    len_r = len(note[0])
    for ci in range(1, len_r//2 + 1):
        if all(r[0:ci] == r[ci:ci*2][::-1] for r in note):
            res.add(ci)
        if all(r[len_r - ci:len_r] == r[len_r - ci * 2:len_r - ci][::-1] for r in note):
            res.add(len_r-ci)
    return res


def get_both_refls(note):
    return get_refls(note), get_refls([''.join(t) for t in zip(*note)])


def get_refls_with_smudge(note, both_refls):
    for ri in range(len(note)):
        for ci in range(len(note[ri])):
            cand_note = [
                r[:ci] + ('#' if r[ci] == '.' else '.') + r[ci+1:] if ri == cri else r
                for cri, r in enumerate(note)
            ]
            cand_refl = get_both_refls(cand_note)
            diff_refls = tuple(map(lambda s1, s2: s1 - s2, cand_refl, both_refls))
            if any(sum(t) > 0 for t in diff_refls):
                return diff_refls


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = [ln.strip() for ln in f.readlines()]

        notes = [list(g) for k, g in groupby(lines, key=lambda ln: bool(ln)) if k]

        refls = [get_both_refls(n) for n in notes]

        r1 = sum([sum(refl_cols) + 100 * sum(refl_rows) for refl_cols, refl_rows in refls])

        r2 = sum([
            sum(refl_cols) + 100 * sum(refl_rows)
            for refl_cols, refl_rows in map(lambda n, r: get_refls_with_smudge(n, r), notes, refls)
        ])

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
