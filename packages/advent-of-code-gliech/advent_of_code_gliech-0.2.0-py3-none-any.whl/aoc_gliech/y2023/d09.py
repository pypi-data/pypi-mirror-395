from itertools import pairwise, starmap
from operator import add, sub
from functools import partial

# Longsolve
# def prep(d):
#     return [list(map(int, l.split())) for l in d.split("\n")]
#
# def part_a(data):
#     predict = lambda ds: ds[-1]+predict([b-a for a,b in pairwise(ds)]) if any(ds) else 0
#     return sum(map(predict, prep(data)))
#
# def part_b(data):
#     predict = lambda ds: ds[0]-predict([b-a for a,b in pairwise(ds)]) if any(ds) else 0
#     return sum(map(predict, prep(data)))

# Higher level solve written out
# def solver(idx, operation):
#     def solve(data):
#         predict = lambda sequence: operation(sequence[idx], predict([b-a for
#                   a,b in pairwise(sequence)])) if any(sequence) else 0
#         return sum(map(predict, prep(data)))
#     return solve

# Golfed
f = lambda i,o: lambda d: sum(map(p:=lambda s: o(s[i], p([b-a for a,b in
    pairwise(s)])) if any(s) else 0, [list(map(int, l.split())) for l in
    d.split("\n")]))
part_a, part_b = starmap(f, ((-1, add), (0, sub)))

if __name__ == "__main__":
    from aoc_gliech import solve
    solve(part_a, part_b)
