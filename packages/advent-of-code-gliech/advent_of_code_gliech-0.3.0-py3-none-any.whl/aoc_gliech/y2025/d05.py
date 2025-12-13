def prep(data):
    fresh_id_str, available_id_str = data.split("\n\n")
    fresh_ids = (map(int, seq.split("-")) for seq in fresh_id_str.split("\n"))
    available_ids = map(int, available_id_str.split("\n"))
    return (fresh_ids, available_ids)

def part_a(data):
    fresh_ids, available_ids = prep(data)
    fresh_ranges = tuple(range(a, b+1) for a, b in fresh_ids)
    return sum(map(lambda a: any(a in r for r in fresh_ranges), available_ids))

def part_b(data):
    sequences = set()
    for low, high in prep(data)[0]:
        consumed_sequences = set()
        for seq in sequences:
            if low>seq[1] or high<seq[0]:
                continue
            low_in_seq = low>=seq[0]
            high_in_seq = high<=seq[1]
            if low_in_seq and high_in_seq:
                break
            consumed_sequences.add(seq)
            if high_in_seq:
                high = seq[1]
            elif low_in_seq:
                low = seq[0]
        else:
            sequences -= consumed_sequences
            sequences.add((low, high))
    return sum(h-l+1 for l, h in sequences)

if __name__ == "__main__":
    from aoc_gliech import solve
    solve(part_a, part_b)
