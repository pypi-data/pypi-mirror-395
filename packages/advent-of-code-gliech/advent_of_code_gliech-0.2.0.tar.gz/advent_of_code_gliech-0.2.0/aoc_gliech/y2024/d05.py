from functools import cmp_to_key, partial
from collections import defaultdict
from operator import eq, ne


def gen_part(op):
    def part(data):
        rules, jobs = map(partial(str.split, sep="\n"), data.split("\n\n"))

        rule_dict = defaultdict(set)
        for key, val in (map(int, rule.split("|")) for rule in rules):
            rule_dict[val].add(key)

        def rule_test(a, b):
            return 1 if b in rule_dict[a] else -1 if a in rule_dict[b] else 0

        jobs = tuple(list(map(int, job.split(","))) for job in jobs)
        sorted_jobs = map(partial(sorted, key=cmp_to_key(rule_test)), jobs)
        filtered_jobs = (i[0] for i in zip(sorted_jobs, jobs) if op(*i))
        return sum(job[len(job)//2] for job in filtered_jobs)

    return part

part_a = gen_part(eq)
part_b = gen_part(ne)

# original solution for part a without sorting
def part_a_orig(data):
    from itertools import starmap
    from collections import deque

    def prep(data):
        data = zip(map(partial(str.split, sep="\n"), data.split("\n\n")), ("|", ","))
        data = starmap(lambda lns, sep: map(lambda ln: tuple(map(int, ln.split(sep))), lns), data)
        return map(tuple, data)

    def middle_page(job):
        return job[len(job)//2]

    rules, jobs = prep(data)

    rule_dict = defaultdict(set)
    for key, val in rules:
        rule_dict[val].add(key)

    def job_ordered(job):
        job = deque(job)
        for _ in range(len(job)):
            rule = rule_dict[job.popleft()]
            if rule & set(job):
                return False
        return True

    return sum(map(middle_page, filter(job_ordered, jobs)))

if __name__ == "__main__":
    from aoc_gliech import solve
    solve(part_a, part_b, part_a_orig)
