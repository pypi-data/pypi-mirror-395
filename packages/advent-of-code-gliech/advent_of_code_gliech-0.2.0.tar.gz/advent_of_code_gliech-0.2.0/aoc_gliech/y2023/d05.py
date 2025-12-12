from functools import partial
from itertools import batched, chain, count, starmap
import yaml

def create_cat(cat_str):
    title, *map_strs = cat_str.split('\n')
    src, _, dst = title.split()[0].split('-')
    map_definitions = [map(int, map_str.split()) for map_str in map_strs]
    mps = {range(src_start, src_start+length): dst_start-src_start for dst_start, src_start, length in map_definitions}
    return (src, {'nxt': dst, 'mps': mps})

def create_reverse_cat(cat_str):
    title, *map_strs = cat_str.split('\n')
    src, _, dst = title.split()[0].split('-')
    map_definitions = [map(int, map_str.split()) for map_str in map_strs]
    mps = {range(dst_start, dst_start+length): src_start-dst_start for dst_start, src_start, length in map_definitions}
    return (dst, {'nxt': src, 'mps': mps})

def map_item(maps, item_id):
    for map_range, offset in maps.items():
        if item_id in map_range:
            return item_id+offset
    else:
        return item_id

def part_a(data):
    seeds, *map_strings = data.split("\n\n")
    items = list(map(int, seeds.split()[1:]))
    cats = dict(map(create_cat, map_strings))
    cur_cat = 'seed'
    while cur_cat != 'location':
        cat = cats[cur_cat]
        items = list(map(partial(map_item, cat['mps']), items))
        cur_cat = cat['nxt']
    return min(items)

def get_items(items, cats, start_cat, end_cat):
    for item in items:
        cur_cat = start_cat
        start_item = item
        while cur_cat != end_cat:
            cat = cats[cur_cat]
            item = map_item(cat['mps'], item)
            cur_cat = cat['nxt']
        yield (start_item, item)

def part_b(data):
    seeds, *map_strings = data.split("\n\n")
    seeds = [range(s, s+l) for s, l in batched(map(int, seeds.split()[1:]), 2)]
    cats = dict(map(create_reverse_cat, map_strings))
    test_item = lambda a: any(a[1] in r for r in seeds)
    min_seed = next(filter(test_item ,get_items(count(), cats, 'location', 'seed')))
    return min_seed[0]


if __name__ == "__main__":
    from aocd import get_data
    print(part_b(get_data(year=2023, day=5)))
