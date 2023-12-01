import re, os, functools

DIR = os.path.dirname(os.path.abspath(__file__))

FILE_PATHS = [
    os.path.join(DIR, 'input_sample.txt'),
    os.path.join(DIR, 'input.txt'),
]


def get_calibration_value(prev, ln):
    fst = re.search(r'\d', ln).group()
    snd = re.search(r'\d', ln[::-1]).group()
    return prev + int(fst + snd)


def main():
    for file_path in FILE_PATHS:
        with open(file_path) as f:
            lines = [l.strip() for l in f.readlines()]

        r1 = functools.reduce(get_calibration_value, lines, 0)

        print(file_path, r1)


if __name__ == "__main__":
    main()
