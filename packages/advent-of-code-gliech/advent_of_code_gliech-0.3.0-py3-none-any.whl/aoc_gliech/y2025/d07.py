from collections import defaultdict

def calc_line_a(line, input_beams):
    output_beams, splits = set(), 0
    for beam in input_beams:
        if line[beam]=="^":
            output_beams |= {beam-1, beam+1}
            splits += 1
        else:
            output_beams.add(beam)
    return output_beams, splits

def part_a(data):
    lines, splits = data.split("\n"), 0
    beam_locations = {lines[0].index("S")}
    for line in lines[1:]:
        beam_locations, line_splits = calc_line_a(line, beam_locations)
        splits += line_splits
    return splits

def calc_line_b(line, input_beams):
    output_beams = defaultdict(int)
    for beam_loc, beam_num in input_beams.items():
        if line[beam_loc]=="^":
            output_beams[beam_loc-1] += beam_num
            output_beams[beam_loc+1] += beam_num
        else:
            output_beams[beam_loc] += beam_num
    return output_beams

def part_b(data):
    lines = data.split("\n")
    beam_locations = defaultdict(int, {lines[0].index("S"): 1})
    for line in lines[1:]:
        beam_locations = calc_line_b(line, beam_locations)
    return sum(beam_locations.values())

if __name__ == "__main__":
    from aoc_gliech import solve
    solve(part_a, part_b)
