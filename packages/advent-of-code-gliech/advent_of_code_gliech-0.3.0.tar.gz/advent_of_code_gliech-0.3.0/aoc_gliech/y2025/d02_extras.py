# Very short solutions using regex
from re import match
from itertools import chain

def part_a(data):
    return sum(num for num in chain.from_iterable(range(a, b+1) for a, b in
           (map(int, seq.split("-")) for seq in data.split(","))) if match(
           r"^(.+)\1$", str(num)) is not None)

def part_b(data):
    return sum(num for num in chain.from_iterable(range(a, b+1) for a, b in
           (map(int, seq.split("-")) for seq in data.split(","))) if match(
           r"^(.+)\1{1,}$", str(num)) is not None)

if __name__ == "__main__":
    from aoc_gliech import solve
    solve(part_a, part_b)
