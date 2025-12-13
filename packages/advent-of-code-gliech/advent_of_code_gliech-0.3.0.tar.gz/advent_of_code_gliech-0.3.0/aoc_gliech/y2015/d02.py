from functools import reduce
from itertools import combinations
from operator import mul

def wrap_order_total(position_fn):
    return lambda data: sum(map(position_fn, (map(int, line.split("x")) for
                        line in data.split("\n"))))

@wrap_order_total
def part_a(pkg_dimensions):
    sides = tuple(mul(*edges) for edges in combinations(pkg_dimensions, 2))
    return 2*sum(sides)+min(sides)

@wrap_order_total
def part_b(pkg_dimensions):
    edges = tuple(pkg_dimensions)
    return 2*sum(sorted(edges)[:2]) + reduce(mul, edges)

if __name__ == "__main__":
    from aoc_gliech import solve
    solve(part_a, part_b)
