from itertools import accumulate, pairwise
from math import ceil, floor
from operator import sub

def prep(data):
    return (int(line[1:])*((line[0]=="R")*2-1) for line in data.split("\n"))

def part_a(data):
    return sum(map(lambda a: a%100==0, accumulate(prep(data), initial=50)))

def part_b(data):
    zero_passes = lambda a: floor(max(a)/100)-ceil(min(a)/100)+(a[0]%100!=0)
    return sum(map(zero_passes, pairwise(accumulate(prep(data), initial=50))))


# earlier solution and less compact form of the main function of part b
from functools import partial

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
    solve(part_a, part_b, partial(part_b_debug, zero_passes_stupid))
