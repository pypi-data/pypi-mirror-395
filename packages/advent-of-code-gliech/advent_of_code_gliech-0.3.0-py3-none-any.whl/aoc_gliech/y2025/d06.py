from operator import add, mul
from functools import reduce

def part_a(data):
    return sum(map(lambda op, nums: reduce(add if op=="+" else mul, map(int,
           nums)), (lines:=[line.split() for line in data.split("\n")])[-1],
           zip(*lines[:-1])))

def part_b_gen(columns):
    for column in map(list, columns):
        last_char = column.pop()
        operand = "".join(column)
        if last_char!=" ":
            operator = add if last_char=="+" else mul
            total = int(operand)
        elif operand.isspace():
            yield total
        else:
            total = operator(total, int(operand))
    yield total

def part_b(data):
    return sum(part_b_gen(zip(*data.split("\n"))))

if __name__ == "__main__":
    from aoc_gliech import solve
    solve(part_a, part_b)
