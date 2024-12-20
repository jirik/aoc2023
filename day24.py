from itertools import combinations
import sys
from shapely import LineString, intersection
import sympy


def get_orthog_isctn(ray, orthog_c, orthog_c_idx):
    coord, deltas = ray
    b_idx = 0 if orthog_c_idx == 1 else 1
    a = coord[orthog_c_idx]
    b = coord[b_idx]
    da = deltas[orthog_c_idx]
    db = deltas[b_idx]
    if a > orthog_c and da > 0 or a < orthog_c and da < 0:
        return None
    return (orthog_c - a) / (da / db) + b


def get_rect_isctn_pts(ray, min_c, max_c):
    result = set()
    for extreme_c in [min_c, max_c]:
        for orthog_c_idx in [0, 1]:
            r = get_orthog_isctn(ray, extreme_c, orthog_c_idx)
            if r is not None and min_c <= r <= max_c:
                c = (extreme_c, r) if orthog_c_idx == 0 else (r, extreme_c)
                result.add(c)
    return result


def get_ln_sg_in_rect(ray, min_c, max_c):
    rect_isctn_pts = get_rect_isctn_pts(ray, min_c, max_c)
    coord, _ = ray
    x, y = coord
    if min_c <= x <= max_c and min_c <= y <= max_c:
        assert len(rect_isctn_pts) == 1
    else:
        assert len(rect_isctn_pts) in [0, 2]  # no corner touch
    if len(rect_isctn_pts) == 1:
        result = (rect_isctn_pts.pop(), coord)
    elif len(rect_isctn_pts) == 2:
        result = tuple(rect_isctn_pts)
    else:
        result = None
    return result


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())

        rays = [tuple(tuple(int(c.strip()) for c in p.split(',')) for p in ln.split('@')) for ln in lines]
        if len(rays) < 10:
            min_c = 7
            max_c = 27
        else:
            min_c = 200000000000000
            max_c = 400000000000000

        rays_xy = [tuple(c[:2] for c in p) for p in rays]

        ray_segments = {ri: get_ln_sg_in_rect(r, min_c, max_c) for ri, r in enumerate(rays_xy)}

        r1 = sum(
            bool(r1_sg and r2_sg and not intersection(LineString(r1_sg), LineString(r2_sg)).is_empty)
            for r1_sg, r2_sg in combinations(ray_segments.values(), 2)
        )

        xs, ys, zs, xd, yd, zd = sympy.symbols("xs, ys, zs, xd, yd, zd", integer=True)
        equations = []
        ts = []
        for idx, ((ray_xs, ray_ys, ray_zs), (ray_xd, ray_yd, ray_zd)) in enumerate(rays[:3]):
            t = sympy.Symbol(f"t{idx}", integer=True)
            ts.append(t)
            equations.append(sympy.Eq(ray_xs + t*ray_xd, xs + t*xd))
            equations.append(sympy.Eq(ray_ys + t*ray_yd, ys + t*yd))
            equations.append(sympy.Eq(ray_zs + t*ray_zd, zs + t*zd))
        solution = sympy.solve(equations, [xs, ys, zs, xd, yd, zd] + ts, dict=True)[0]
        r2 = solution[xs] + solution[ys] + solution[zs]

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
