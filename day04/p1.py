import re, os, math

DIR = os.path.dirname(os.path.abspath(__file__))

FILE_PATHS = [
    os.path.join(DIR, 'input_sample.txt'),
    os.path.join(DIR, 'input.txt'),
]


def get_line_points(ln):
    left, right = ln.split(':')[1].split('|')
    lefts = re.findall(r'\d+', left)
    rights = re.findall(r'\d+', right)
    winners_count = len([n for n in rights if n in lefts])
    return round(math.pow(2, winners_count - 1)) if winners_count else 0


def main():
    for file_path in FILE_PATHS:
        with open(file_path) as f:
            lines = [ln.strip() for ln in f.readlines()]

        r1 = sum([get_line_points(ln) for ln in lines])

        print(file_path, r1)


if __name__ == "__main__":
    main()
