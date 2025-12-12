def false_id_selector(id_gen):
    def solver(data):
        prep = (map(int, seq.split("-")) for seq in data.split(","))
        ranges = tuple(range(a, b+1) for a, b in prep)
        real_id = lambda a: any(a in id_range for id_range in ranges)
        return sum(set(filter(real_id, id_gen(max(rg.stop for rg in ranges)))))
    return solver

@false_id_selector
def part_a(end):
    for i in range(1, end//10**(len(str(end))//2)+1):
        yield int(str(i)*2)

@false_id_selector
def part_b(end):
    for num_length in range(2, len(str(end))+1):
        factors = filter(lambda a: num_length%a==0, range(1, num_length//2+1))
        for factor in factors:
            rev_factor = num_length//factor
            for pattern in range(max(1, 10**(factor-1)), 10**factor):
                yield int(str(pattern)*rev_factor)

if __name__ == "__main__":
    from aoc_gliech import solve
    solve(part_a, part_b)
