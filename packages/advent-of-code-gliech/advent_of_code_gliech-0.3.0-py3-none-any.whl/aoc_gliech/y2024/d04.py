import numpy as np
import re
from functools import partial
from itertools import chain
from scipy.ndimage import generic_filter

def all_directions(solver):
    def decorated(data):
        word_field = np.array([list(line) for line in data.split("\n")], dtype='U1')
        return sum(map(solver, map(partial(np.rot90, word_field), range(4))))
    return decorated

@all_directions
def part_a(word_field):
    diag_max = max(word_field.shape)-4
    diag_range = range(-diag_max, diag_max+1)
    all_lines = chain(word_field, map(word_field.diagonal, diag_range))
    return sum(map(lambda a: len(re.findall("XMAS", ''.join(a))), all_lines))

masmas_shape = [[1, 0, 1],
                [0, 1, 0],
                [1, 0, 1]]
masmas_values = np.frombuffer(b"MSAMS", dtype=np.uint8)

@all_directions
def part_b(word_field):
    word_field.dtype = np.int32
    findings = generic_filter(word_field, partial(np.array_equal, masmas_values),
                              footprint=masmas_shape, mode="constant")
    return int(np.sum(findings))

if __name__ == "__main__":
    from aoc_gliech import solve
    solve(part_a, part_b)
