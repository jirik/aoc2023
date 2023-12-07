from collections import Counter
from functools import reduce
import re, os, math

DIR = os.path.dirname(os.path.abspath(__file__))

FILE_PATHS = [
    os.path.join(DIR, 'input_sample.txt'),
    os.path.join(DIR, 'input.txt'),
]


CARDS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'][::-1]


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
        print(file_path, r1)


if __name__ == "__main__":
    main()
