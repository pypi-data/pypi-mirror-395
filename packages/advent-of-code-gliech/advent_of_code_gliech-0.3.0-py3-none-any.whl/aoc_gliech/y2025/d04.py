import numpy as np
from scipy.ndimage import generic_filter

def prep(data):
    return np.array([[char=="@" for char in line] for line in data.split("\n")])

def part_a(data):
    nice_roll = lambda a: a[4] and sum(a)<5
    nice_rolls = generic_filter(prep(data), nice_roll, size=3, mode="constant")
    return int(np.sum(nice_rolls))

def part_b(data):
    room = prep(data)
    last_roll_count = 0
    next_roll_count = np.sum(room)
    init_roll_count = next_roll_count
    remove_rolls = lambda a: a[4] and sum(a)>=5
    while last_roll_count != next_roll_count:
        last_roll_count = next_roll_count
        room = generic_filter(room, remove_rolls, size=3, mode="constant")
        next_roll_count = np.sum(room)
    return int(init_roll_count - last_roll_count)

if __name__ == "__main__":
    from aoc_gliech import solve
    solve(part_a, part_b)
