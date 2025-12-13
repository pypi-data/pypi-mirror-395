from functools import partial

def prep(data):
    return (tuple(map(int, line)) for line in data.split("\n"))

def calc_line(digits, line):
    last_index, result = 0, 0
    for i in reversed(range(digits)):
        digit = max(line[last_index:len(line)-i])
        last_index += line[last_index:].index(digit)+1
        result = result*10+digit
    return result

def gen_part(digits):
    return lambda d: sum(map(partial(calc_line, digits), prep(d)))

part_a, part_b = map(gen_part, (2, 12))

if __name__ == "__main__":
    from aoc_gliech import solve
    solve(part_a, part_b)
