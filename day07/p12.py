from collections import Counter
from functools import reduce
import re, os, math

DIR = os.path.dirname(os.path.abspath(__file__))

FILE_PATHS = [
    os.path.join(DIR, 'input_sample.txt'),
    os.path.join(DIR, 'input.txt'),
]


CARDS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'][::-1]
CARDS_2 = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J'][::-1]


def main():
    for file_path in FILE_PATHS:
        with open(file_path) as f:
            lines = [ln.strip() for ln in f.readlines()]

        tuples = [tuple(ln.split(' ')) for ln in lines]

        sorted_tuples = sorted(tuples, key=lambda t: (
            tuple(sorted(Counter(t[0]).values(), reverse=True)),
            tuple(CARDS.index(char) for char in t[0])
        ))
        r1 = sum([(idx+1)*int(b) for idx, (_, b) in enumerate(sorted_tuples)])

        tuples2 = [
            (c, b, sorted([c.replace('J', subst) for subst in CARDS_2[1:]],
                          key=lambda c: tuple(sorted(Counter(c).values(), reverse=True)))[-1])
            for c, b in tuples
        ]
        sorted_tuples2 = sorted(tuples2, key=lambda t: (
            tuple(sorted(Counter(t[2]).values(), reverse=True)),
            tuple(CARDS_2.index(char) for char in t[0])
        ))
        r2 = sum([(idx + 1) * int(b) for idx, (_, b, _) in enumerate(sorted_tuples2)])

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
