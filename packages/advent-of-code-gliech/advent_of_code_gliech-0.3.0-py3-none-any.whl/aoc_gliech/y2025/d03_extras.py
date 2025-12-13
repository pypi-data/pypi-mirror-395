from aoc_gliech.y2025.d03 import prep

# earlier solution for the central function of part a
def line_value(line):
    d1 = max(line[:-1])
    d2 = max(line[line.index(d1)+1:])
    return d1*10+d2

def part_a(data):
    return sum(map(line_value, prep(data)))

if __name__ == "__main__":
    from aoc_gliech import solve
    solve(part_a)
