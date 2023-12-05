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


def find_location2(seeds, maps):
    for mp in maps:
        new_seeds = []
        while seeds:
            seed_s, seed_e = seeds.pop(0)
            m = next(((drs, srs, rl) for drs, srs, rl in mp if seed_s <= srs + rl - 1 and seed_e >= srs), None)
            if m is None:
                new_seeds.append((seed_s, seed_e))
            else:
                drs, srs, rl = m
                int_s = max(seed_s, srs)
                int_e = min(seed_e, srs + rl - 1)
                if int_s > seed_s:
                    seeds.append((seed_s, int_s-1))
                if int_e < seed_e:
                    seeds.append((int_e + 1, seed_e))
                new_seeds.append((int_s - srs + drs, int_e - srs + drs))
        seeds = new_seeds
    return new_seeds


def main():
    for file_path in FILE_PATHS:
        with open(file_path) as f:
            lines = [ln.strip() for ln in f.readlines()]

        seeds = [int(n) for n in lines[0].split(': ')[1].split(' ')]
        maps = read_maps(lines[3:])

        r1 = min([find_location(s, maps) for s in seeds])
        seeds = [(seeds[idx*2], seeds[idx*2] + seeds[idx*2+1] - 1) for idx in range(len(seeds)//2)]
        r2 = min([loc for loc, _ in find_location2(seeds, maps)])
        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
