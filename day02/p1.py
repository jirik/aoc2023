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


def main():
    for file_path in FILE_PATHS:
        with open(file_path) as f:
            lines = [ln.strip() for ln in f.readlines()]

        r1 = functools.reduce(reduce_line, lines, 0)

        print(file_path, r1)


if __name__ == "__main__":
    main()
