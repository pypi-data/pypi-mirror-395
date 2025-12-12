from functools import partial

def prep(data):
    return (tuple(map(int, line)) for line in data.split("\n"))

def line_value(line, digits):
    last_index, result = 0, 0
    for i in reversed(range(digits)):
        digit = max(line[last_index:len(line)-i])
        last_index += line[last_index:].index(digit)+1
        result = result*10+digit
    return result

def part_a(data):
    return sum(map(partial(line_value, digits=2), prep(data)))

def part_b(data):
    return sum(map(partial(line_value, digits=12), prep(data)))


# earlier solution for the central function of part a
def line_value_part_a(line):
    d1 = max(line[:-1])
    d2 = max(line[line.index(d1)+1:])
    return d1*10+d2

if __name__ == "__main__":
    from aoc_gliech import solve
    solve(part_a, part_b)
