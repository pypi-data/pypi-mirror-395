from functools import cache
from numpy import array as arr, where

def prep(data):
    data = data.split('\n')
    return arr([list(line) for line in data], dtype='U1')

pipe_openings = {
    (0, 1): "7-J",
    (0, -1): "L-F",
    (1, 0): "J|L",
    (-1, 0): "7|F"}

def turn_360_degrees(direction):
    return tuple(x*-1 for x in direction)

@cache
def pipe_in_out(char, in_direction):
    mirror_out_direction = next(k for k,v in pipe_openings.items() if k!=in_direction and char in v)
    return turn_360_degrees(mirror_out_direction)

def get_loop(tiles):
    start_pos = arr(next(zip(*where(tiles == "S"))))
    loop = {tuple(start_pos)}

    for start_direction, allowed_connections in pipe_openings.items():
        current_pos = start_pos+arr(start_direction)
        current_char = tiles[*current_pos]
        if current_char in allowed_connections:
            direction = start_direction
            break

    while current_char != "S":
        loop.add(tuple(current_pos))
        direction = pipe_in_out(current_char, direction)
        current_pos += direction
        current_char = tiles[*current_pos]

    possible_start_pipes = set(pipe_openings[turn_360_degrees(start_direction)])
    possible_end_pipes = set(pipe_openings[direction])
    tiles[*start_pos] = (possible_start_pipes & possible_end_pipes).pop()

    return loop

def part_a(data):
    return len(get_loop(prep(data)))//2

def part_b(data):
    tiles = prep(data)
    loop = get_loop(tiles)
    along_loop = {
            "L": "7",
            "F": "J"
            }
    enclosed = 0

    for i in range(tiles.shape[0]):
        inside_loop = False
        for j, char in enumerate(tiles[i]):
            if (i, j) in loop:
                if char in along_loop.keys():
                    on_loop = char
                elif char in along_loop.values():
                    inside_loop = inside_loop != (along_loop[on_loop] == char)
                elif char == "|":
                    inside_loop = not inside_loop
            elif inside_loop:
                enclosed +=1
    return enclosed

if __name__ == "__main__":
    from aoc_gliech import solve
    test = """
        7-F-7-
        .FJ.|7
        SJL.L7
        |F---J
        LJ..LJ
        """
    solve(part_a, part_b, data=test)
