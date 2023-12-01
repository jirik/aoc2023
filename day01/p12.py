import re, os, functools

DIR = os.path.dirname(os.path.abspath(__file__))

FILE_PATHS = [
    os.path.join(DIR, 'input_sample.txt'),
    os.path.join(DIR, 'input_sample2.txt'),
    os.path.join(DIR, 'input.txt'),
]

DIGITS = [
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine',
]


def get_calibration_subvalue(ln, pattern):
    digit_str = re.search(pattern, ln).group(1)
    digit = DIGITS.index(digit_str) + 1 if digit_str in DIGITS else int(digit_str)
    return digit


def get_calibration_value(prev, ln):
    digits_pattern = '|'.join(DIGITS)
    fst = get_calibration_subvalue(ln, f'(\\d|{digits_pattern})')
    snd = get_calibration_subvalue(ln, f'(?:.*)(\\d|{digits_pattern})')
    return prev + int(f"{fst}{snd}")


def main():
    for file_path in FILE_PATHS:
        with open(file_path) as f:
            lines = [l.strip() for l in f.readlines()]

        r1 = functools.reduce(get_calibration_value, lines, 0)

        print(file_path, r1)


if __name__ == "__main__":
    main()
