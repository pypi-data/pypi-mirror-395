from functools import reduce
from itertools import starmap
from operator import mul
from math import ceil, floor, sqrt

def race(time, distance):
    x = sqrt(time**2 - 4*distance)
    min_win = floor((time-x)/2 + 1)
    max_win = ceil((time+x)/2 - 1)
    return max_win-min_win+1

def part_a(data):
    d = zip(*(map(int, v.split()[1:]) for v in data.split("\n")))
    return reduce(mul, starmap(race, d))

def part_b(data):
    d = [int("".join(v.split()[1:])) for v in data.split("\n")]
    return race(*d)

if __name__ == "__main__":
    from aocd import get_data
    print(part_b(get_data()))
