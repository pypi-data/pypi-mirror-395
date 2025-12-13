import re
from operator import mul

def part_a(data):
    return sum(mul(*map(int, pair)) for pair in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", data))

def part_b(data):
    return sum(map(part_a, re.findall(r"(?:do\(\)|^).*?(?:don't\(\)|$)", data, flags=re.DOTALL)))

if __name__ == "__main__":
    from aoc_gliech import solve
    solve(part_a, part_b)
