from functools import reduce
import re, os, math, sys


def get_cycle(seq, lmap, rmap, cnode):
    pth = []
    step = 0
    z_idxs = []
    while not (len(z_idxs) == 1 and cnode and cnode[-1] == 'Z'):
        pth.append(cnode)
        if cnode[-1] == 'Z':
            z_idxs.append(step)
        move = seq[step % len(seq)]
        mp = lmap if move == 'L' else rmap
        cnode = mp[cnode]
        step += 1
    return z_idxs[0], len(pth) - z_idxs[0]


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = [ln.strip() for ln in f.readlines()]

        seq = lines[0]
        tuples = [
            (ln[0:3], ln[7:10], ln[12:15])
            for ln in lines[2:]
        ]
        lmap, rmap = reduce(lambda pr, t: (pr[0] | {t[0]: t[1]}, pr[1] | {t[0]: t[2]}), tuples, ({}, {}))

        cnode = 'AAA'
        step = 0
        while 'ZZZ' != cnode:
            move = seq[step % len(seq)]
            mp = lmap if move == 'L' else rmap
            cnode = mp[cnode]
            step += 1

        r1 = step

        cycles = [get_cycle(seq, lmap, rmap, n) for n in lmap if n[-1] == 'A']

        # so we can ignore offset-related logic
        assert all(offset == cycle_len for offset, cycle_len in cycles)

        r2 = math.lcm(*[c[0] for c in cycles])
        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
