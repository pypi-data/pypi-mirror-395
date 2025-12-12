from functools import reduce
from collections import defaultdict
def prep(data):
    return data.split(",")

def hash_algo(s):
    return reduce(lambda x,y: (x+ord(y))*17%256, s, 0)

def part_a(data):
    return sum(map(hash_algo, prep(data)))

def part_b(data):
    boxes = defaultdict(dict)
    for line in prep(data):
        instruction = line.split("=")
        if len(instruction) == 1:
            label = instruction[0][:-1]
            box = hash_algo(label)
            if label in boxes[box]:
                del boxes[box][label]
        else:
            label = instruction[0]
            box = hash_algo(label)
            boxes[box][label] = int(instruction[1])
    return sum(sum((box+1)*(slot+1)*focal_len for slot, focal_len in enumerate(lenses.values())) for box, lenses in boxes.items())

if __name__ == "__main__":
    from aoc_gliech import solve
    solve(part_a, part_b)
