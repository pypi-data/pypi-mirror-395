# functional solution
from collections import Counter
from functools import reduce
from operator import iadd

gs = lambda d: reduce(lambda i,l:(reduce(iadd,b:=[{a[0]-1:a[1],a[0]+1:a[1]}if
     l[a[0]]=="^"else{a[0]:a[1]}for a in i[0].items()],Counter()),i[1]+sum(len(
     a)>1 for a in b)),s:=d.split("\n"),(Counter([s[0].index("S")]),0))
part_a, part_b = lambda d: gs(d)[1], lambda d: gs(d)[0].total()

# longer version
# def solve_line(input_state, line):
#     split_beam = lambda a: {a[0]-1:a[1],a[0]+1:a[1]} if line[a[0]]=="^" else {a[0]:a[1]}
#     beams = tuple(map(split_beam, input_state[0].items()))
#     return reduce(iadd, beams, Counter()), input_state[1]+sum(len(a)>1 for a in beams)

# def general_solver(data):
#     lines = data.split("\n")
#     return reduce(solve_line, lines[1:], (Counter([lines[0].index("S")]), 0))

# def part_a(data):
#     return general_solver(data)[1]

# def part_b(data):
#     return general_solver(data)[0].total()

if __name__ == "__main__":
    from aoc_gliech import solve
    solve(part_a, part_b)
