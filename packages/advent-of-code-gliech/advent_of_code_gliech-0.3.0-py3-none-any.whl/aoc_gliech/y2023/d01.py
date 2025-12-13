import re

def prep(data):
    return data.split("\n")

def part_a(data):
    return sum(int((d:=re.findall(r"\d", line))[0]+d[-1]) for line in prep(data))

def part_b(data):
    match = ["\\d", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    return sum((f:=lambda p: int(n) if len(n:=re.match(f"(?:.*{p})({"|".join(match)})", l).group(1))==1 else match.index(n))("?")*10+f("") for l in prep(data))

if __name__ == "__main__":
    from aoc_gliech import solve
    custom_data = """
    two1nine6
    eightwo77eighthree
    abcone2three7xyz
    xtwone34four
    4nineeightseven2
    zoneight234
    7pqrstsixteen
    """
    solve(part_a, part_b, data=custom_data)
