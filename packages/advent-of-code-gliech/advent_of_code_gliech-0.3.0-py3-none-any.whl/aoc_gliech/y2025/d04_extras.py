import numpy as np
from scipy.ndimage import generic_filter

def part_a_oneline(d):
    return int(np.sum(generic_filter(np.array([[c=="@"for c in l]for l in
           d.split("\n")]),lambda a:a[4]and sum(a)<5,3,mode="constant")))

if __name__ == "__main__":
    from aoc_gliech import solve
    solve(part_a_oneline)
