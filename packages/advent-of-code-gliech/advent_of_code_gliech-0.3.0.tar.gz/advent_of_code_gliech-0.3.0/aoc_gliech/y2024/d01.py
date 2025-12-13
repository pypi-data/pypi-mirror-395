from collections import Counter

def prep(data):
    return zip(*[map(int, pair.split()) for pair in data.split("\n")])

def part_a(data):
    return sum(abs(a-b) for a, b in zip(*map(sorted, prep(data))))

def part_b(data):
    list_a, list_b = prep(data)
    lookup_table = Counter(list_b)
    return sum(lookup_table[num]*num for num in list_a)

if __name__ == "__main__":
    from aoc_gliech import solve
    solve(part_a, part_b)
