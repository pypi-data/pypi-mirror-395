from itertools import accumulate, pairwise
from math import ceil, floor

def prep(data):
    return (int(line[1:])*((line[0]=="R")*2-1) for line in data.split("\n"))

def part_a(data):
    return sum(map(lambda a: a%100==0, accumulate(prep(data), initial=50)))

def part_b(data):
    zero_passes = lambda a: floor(max(a)/100)-ceil(min(a)/100)+(a[0]%100!=0)
    return sum(map(zero_passes, pairwise(accumulate(prep(data), initial=50))))

if __name__ == "__main__":
    from aoc_gliech import solve
    solve(part_a, part_b)
