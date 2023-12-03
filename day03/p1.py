import re, os

DIR = os.path.dirname(os.path.abspath(__file__))

FILE_PATHS = [
    os.path.join(DIR, 'input_sample.txt'),
    os.path.join(DIR, 'input.txt'),
]


def get_rect_coords(row_idx, col_idx1, col_idx2):
    return {(r, c) for r in range(row_idx-1, row_idx+2) for c in range(col_idx1-1, col_idx2+2)}


def read_coords(pattern, lines):
    return [
        (m.group(), ln_idx, m.start(), m.end() - 1)
        for ln_idx, ln in enumerate(lines) for m in re.finditer(pattern, ln)
    ]


def main():
    for file_path in FILE_PATHS:
        with open(file_path) as f:
            lines = [ln.strip() for ln in f.readlines()]

        all_symbol_coords = {(r, c) for _, r, c, _ in read_coords(r'[^.0-9]+', lines)}
        coords_per_number = [(n, get_rect_coords(*coords)) for n, *coords in read_coords(r'\d+', lines)]

        r1 = sum(int(n) for n, n_coords in coords_per_number if bool(n_coords & all_symbol_coords))
        print(file_path, r1)


if __name__ == "__main__":
    main()
