import re
from functools import cache, partial
from itertools import cycle
from math import lcm
from operator import methodcaller as mc

@cache
def prep(data):
    directions, map_str = data.split("\n\n")
    map_nodes = {a: b for a, *b in map(partial(re.findall, r"\w+"), map_str.split("\n"))}
    return directions, map_nodes

def travel(data, start, end):
    directions, map_nodes = prep(data)
    directions = cycle(directions)
    cur_node = start
    steps = 0
    while not cur_node.endswith(end):
        steps += 1
        cur_node = map_nodes[cur_node][int(next(directions) == "R")]
    return steps

part_a = partial(travel, start="AAA", end="ZZZ")
part_b = lambda d: lcm(*map(partial(travel, d, end="Z"), filter(mc("endswith", "A"), prep(d)[1])))

if __name__ == "__main__":
    # from aocd import get_data
    from aoc_gliech.util import data
    print([d[-1] for d in data()])
    test = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""
