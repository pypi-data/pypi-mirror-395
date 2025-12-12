def prep(data):
    lab = {}
    for idx_x, line in enumerate(data.split("\n")):
        for idx_y, char in enumerate(line):
            coord = complex(idx_x, idx_y)
            lab[coord] = char
            if char == "^":
                vec = coord, -1
    return lab, vec

def run_guard(lab, vec, path):
    while True:
        next_pos = sum(vec)
        if vec in path:
            return True
        path.add(vec)
        if next_pos not in lab:
            return False
        vec = (vec[0], vec[1]*-1j) if lab[next_pos] == "#" else (next_pos, vec[1])

def path_coords(lab, vec):
    path = set()
    run_guard(lab, vec, path=path)
    return set(vec[0] for vec in path)

def block_path(lab, coord):
    lab[coord] = "#"
    return lab

def part_a(data):
    return len(path_coords(*prep(data)))

def part_b_shorter(data):
    lab, vec = prep(data)
    coords = path_coords(lab, vec)
    coords.remove(vec[0])
    return sum(run_guard(block_path(lab.copy(), i), vec, set()) for i in coords)

def part_b_faster(data):
    lab, vec = prep(data)
    path, path_coords, loops = set(), set(), 0
    while True:
        next_pos = sum(vec)
        if next_pos not in lab:
            return loops
        if lab[next_pos] == "." and next_pos not in path_coords:
            lab[next_pos] = "#"
            loops += run_guard(lab, vec, path.copy())
            lab[next_pos] = "."
        path.add(vec)
        path_coords.add(vec[0])
        vec = (vec[0], vec[1]*-1j) if lab[next_pos] == "#" else (next_pos, vec[1])

part_b = part_b_faster

if __name__ == "__main__":
    from aoc_gliech import solve
    solve(part_a, part_b)
