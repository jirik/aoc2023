import os, functools

DIR = os.path.dirname(os.path.abspath(__file__))

FILE_PATHS = [
    os.path.join(DIR, 'input_sample.txt'),
    os.path.join(DIR, 'input.txt'),
]

CUBES = {
    'red': 12,
    'green': 13,
    'blue': 14,
}


def reduce_line(prev, ln):
    game_label, game = ln.split(': ')
    game_id = int(game_label.split(' ')[-1])
    for rnd in game.split('; '):
        for cube in rnd.split(', '):
            cnt_str, color = cube.split(' ')
            cnt = int(cnt_str)
            if CUBES[color] < cnt:
                return prev
    return prev + game_id


def reduce_line_part2(prev, ln):
    game = ln.split(': ')[-1]
    counts = {k: 0 for k in CUBES}
    for rnd in game.split('; '):
        for cube in rnd.split(', '):
            cnt_str, color = cube.split(' ')
            cnt = int(cnt_str)
            counts[color] = max(cnt, counts[color])
    return prev + functools.reduce(lambda x, y: x*y, counts.values())


def main():
    for file_path in FILE_PATHS:
        with open(file_path) as f:
            lines = [ln.strip() for ln in f.readlines()]

        r1 = functools.reduce(reduce_line, lines, 0)
        r2 = functools.reduce(reduce_line_part2, lines, 0)

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
