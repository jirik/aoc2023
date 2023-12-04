import functools, re, os, math

DIR = os.path.dirname(os.path.abspath(__file__))

FILE_PATHS = [
    os.path.join(DIR, 'input_sample.txt'),
    os.path.join(DIR, 'input.txt'),
]


def get_line_winners(ln):
    left, right = ln.split(':')[1].split('|')
    lefts = re.findall(r'\d+', left)
    rights = re.findall(r'\d+', right)
    return len([n for n in rights if n in lefts])


def get_line_points(ln):
    winners_count = get_line_winners(ln)
    return round(math.pow(2, winners_count - 1)) if winners_count else 0


def reduce_part2(prev, ln):
    num_copies, copies_list = prev
    current_copies = (copies_list.pop(0) if copies_list else 0) + 1
    num_copies += current_copies
    winners = get_line_winners(ln)
    for idx in range(winners):
        if idx == len(copies_list):
            copies_list.append(0)
        copies_list[idx] += current_copies
    return num_copies, copies_list


def main():
    for file_path in FILE_PATHS:
        with open(file_path) as f:
            lines = [ln.strip() for ln in f.readlines()]

        r1 = sum([get_line_points(ln) for ln in lines])
        r2, _ = functools.reduce(reduce_part2, lines, (0, []))

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
