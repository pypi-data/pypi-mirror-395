from collections import defaultdict
from functools import reduce
from itertools import batched
from operator import mul
import re

def prep(data):
    def group_cubes(cubes):
        groups = defaultdict(int)
        for num, color in cubes: groups[color] = max(int(num), groups[color])
        return groups
    return (group_cubes(batched(re.findall(r"[\d\w]+", game.split(":")[1]), 2)) for game in data.split("\n"))

def part_a(data):
    # input = [[{(c := cubes.split(" "))[1]: int(c[0]) for cubes in draw.split(", ")} for draw in game.split(": ")[1].split("; ")] for game in data.split("\n")]
    # return sum(index+1 for index, game in enumerate(input) if not any(starmap(lambda color, num: num > ["red", "green", "blue"].index(color)+12, chain.from_iterable(map(methodcaller("items"), game)))))
    return sum(index+1 for index, game in enumerate(prep(data)) if all(num < ("red", "green", "blue").index(color)+13 for color, num in game.items()))

def part_b(data):
    return sum(reduce(mul, game.values()) for game in prep(data))

if __name__ == "__main__":
    from aoc_gliech import solve
    solve(prep, part_a, part_b)
