import numpy as np
import re
from collections import defaultdict
from itertools import starmap
from operator import itemgetter, mul

is_symbol = np.vectorize(lambda a: a!='.' and not a.isdigit())

def potential_parts(data):
    data = data.split('\n')
    arr = np.array([list(line) for line in data], dtype='U1')
    for idx, line in enumerate(data):
        for match in re.finditer(r'\d+', line):
            h_min = max(0, idx-1)
            h_max = min(arr.shape[0], idx+2)
            w_min = max(0, match.start()-1)
            w_max = min(arr.shape[1], match.end()+1)
            neighbourhood = arr[h_min:h_max,w_min:w_max]
            yield int(match.group()), neighbourhood

def part_a(data):
    return sum(part[0] for part in potential_parts(data) if is_symbol(part[1]).any())


def get_potential_gears(data):
    data = data.split('\n')
    arr = np.array([list(line) for line in data], dtype='U1')
    for idx, line in enumerate(data):
        for match in re.finditer(r'\d+', line):
            h_min = max(0, idx-1)
            h_max = min(arr.shape[0], idx+2)
            w_min = max(0, match.start()-1)
            w_max = min(arr.shape[1], match.end()+1)
            neighbourhood = arr[h_min:h_max,w_min:w_max]
            for h, w in zip(*np.where(neighbourhood=='*')):
                yield (h_min+h, w_min+w), int(match.group())

def part_b(data):
    potential_gears = defaultdict(list)
    for loc, part in get_potential_gears(data):
        potential_gears[loc].append(part)
    gears = filter(lambda parts: len(parts)==2, potential_gears.values())
    return sum(starmap(mul, gears))


if __name__ == "__main__":
    from aoc_gliech import solve
    solve(part_a, part_b)
