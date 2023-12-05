import functools, re, os, math

DIR = os.path.dirname(os.path.abspath(__file__))

FILE_PATHS = [
    os.path.join(DIR, 'input_sample.txt'),
    os.path.join(DIR, 'input.txt'),
]


def read_maps(lns):
    result = []
    current_map = []
    while lns:
        ln = lns.pop(0)
        if not ln:
            result.append(current_map)
            current_map = []
            lns.pop(0)
        else:
            current_map.append([int(n) for n in ln.split(' ')])
    result.append(current_map)
    return result


def find_location(seed, maps):
    for mp in maps:
        new_seed = next((seed - srs + drs for drs, srs, rl in mp if srs <= seed < srs + rl), None)
        seed = new_seed if new_seed is not None else seed
    return seed


def main():
    for file_path in FILE_PATHS:
        with open(file_path) as f:
            lines = [ln.strip() for ln in f.readlines()]

        seeds = [int(n) for n in lines[0].split(': ')[1].split(' ')]
        maps = read_maps(lines[3:])

        r1 = min([find_location(s, maps) for s in seeds])
        print(file_path, r1)


if __name__ == "__main__":
    main()
