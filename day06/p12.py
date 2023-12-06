from functools import reduce
import re, os, math

DIR = os.path.dirname(os.path.abspath(__file__))

FILE_PATHS = [
    os.path.join(DIR, 'input_sample.txt'),
    os.path.join(DIR, 'input.txt'),
]


def get_race_ways(race):
    tm, dst = race
    wins = 0
    for t in range(tm):
        if t*(tm-t) > dst:
            wins += 1
    return wins


def main():
    for file_path in FILE_PATHS:
        with open(file_path) as f:
            lines = [ln.strip() for ln in f.readlines()]

        times, dists = [[int(n) for n in re.split(' +', ln.split(':')[1].strip())] for ln in lines]
        races = list(zip(times, dists))
        r1 = reduce(lambda x, y: x*y, [get_race_ways(r) for r in races])

        race = [int(''.join(re.findall(r'\d+', ln))) for ln in lines]
        r2 = get_race_ways(race)

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
