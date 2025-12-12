import numpy as np
from itertools import combinations, starmap
from operator import sub

custom_data = """
        ....
        .#..
        ...#
        ....
        ...#"""

def prep(data):
    return np.array([list(line) for line in data.split('\n')], dtype='U1')

def expand(image):
    for axis in 0, 1:
        empty_spaces = np.where(np.all(image == ".", axis))[0]
        image = np.insert(image, empty_spaces, ".", axis=1-axis)
    return image

def galaxy_distances(image):
    return map(sum, map(np.abs, starmap(sub, combinations(map(np.array, zip(*np.where(image == "#"))), 2))))

def part_a(data):
    return sum(galaxy_distances(expand(prep(data))))

def part_b(data):
    image = prep(data)
    dist_past = galaxy_distances(image)
    dist_now = galaxy_distances(expand(image))
    return sum(starmap(lambda a, b: a+(b-a)*999999, zip(dist_past, dist_now)))

if __name__ == "__main__":
    from aoc_gliech import solve
    solve(part_a, part_b, data=custom_data)
