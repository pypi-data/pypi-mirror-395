# earlier solution and less compact form of the main function of part b
from itertools import accumulate, pairwise
from math import ceil, floor
from functools import partial
from aoc_gliech.y2025.d01 import prep

def zero_passes_stupid(a):
    direction = (a[0]<a[1])*2-1
    movement = range(a[0], a[1]+direction, direction)
    return sum(map(lambda a: a%100==0, movement)) - (a[0]%100==0)

def zero_passes_debug(a):
    # result = abs(sub(*map(lambda b: b//100, a))) - (a[0]%100==0)
    low, high = sorted(a)
    result = floor(high/100) - ceil(low/100) + 1 - (a[0]%100==0)
    # print(f"{a[0]:4d} -> {a[1]:4d} = {result:2d}")
    return(result)

def part_b_debug(pass_counter, data):
    return sum(map(pass_counter, pairwise(accumulate(prep(data), initial=50))))

if __name__ == "__main__":
    from aoc_gliech import solve
    solve(partial(part_b_debug, zero_passes_stupid),
          partial(part_b_debug, zero_passes_debug))
