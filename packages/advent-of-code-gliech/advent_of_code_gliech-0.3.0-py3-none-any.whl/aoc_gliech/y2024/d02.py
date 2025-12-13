from itertools import pairwise
from math import copysign
from operator import sub

def prep(data):
    return (list(map(int, line.split())) for line in data.split("\n"))

def test_pair(pair):
    diff = sub(*pair)
    return copysign(1 <= abs(diff) <= 3, diff)

def test_report_a(report):
    return len(report)-1 == abs(sum(map(test_pair, pairwise(report))))

def part_a(data):
    return sum(map(test_report_a, prep(data)))

def test_report_a_iter(report):
    last_num = None
    first_valid_test = None
    for num in report:
        if last_num is not None:
            test = test_pair((last_num, num))
            if test == 0:
                return False
            else:
                if first_valid_test is None:
                    first_valid_test = test
                elif first_valid_test != test:
                    return False
        last_num = num
    return True

def part_a_iter(data):
    sum_safe = 0
    for report in prep(data):
        report = list(report)
        if test_report_a_iter(report):
            sum_safe +=1
    return sum_safe

def test_report_b(report):
    dampener_used = False
    last_num = None
    first_valid_test = None
    for num in report:
        if last_num is not None:
            test = test_pair((last_num, num))
            if test == 0:
                if dampener_used:
                    return False
                else:
                    dampener_used = True
                    continue
            else:
                if first_valid_test is None:
                    first_valid_test = test
                elif first_valid_test != test:
                    if dampener_used:
                        return False
                    else:
                        dampener_used = True
                        continue
        last_num = num
    return True

def part_b(data):
    sum_safe = 0
    for report in prep(data):
        report = list(report)
        if test_report_b(report) or test_report_b(reversed(report)):
            sum_safe +=1

    return sum_safe

if __name__ == "__main__":
    from aoc_gliech import solve
    solve(part_a, part_b)
