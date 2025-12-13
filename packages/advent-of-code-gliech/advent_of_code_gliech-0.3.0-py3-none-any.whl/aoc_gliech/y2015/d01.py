from collections import Counter
from operator import sub

def prep(data):
    return data.split("\n")

def part_a(data):
    return sub(*Counter(data).values())

def part_b(data):
    cur_floor = 0
    for idx, char in enumerate(data):
        cur_floor += (char=="(")*2-1
        if cur_floor < 0:
            return idx+1

if __name__ == "__main__":
    from aoc_gliech import solve
    solve(part_a, part_b)
