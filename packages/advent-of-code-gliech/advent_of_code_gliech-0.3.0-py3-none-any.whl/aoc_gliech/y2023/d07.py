from collections import Counter
from operator import call
from functools import partial
from itertools import starmap

# def winnings(counter, card_order, data):
#     tie_value = lambda hand: sum(list(card_order).index(value)<<idx*4 for idx, value in enumerate(reversed(hand)))
#     hand_value = lambda hand: (sum(value**2 for value in counter(hand).values())<<20)+tie_value(hand)
#     hands = (starmap(call, zip((hand_value, int), line.split())) for line in data.split("\n"))
#     return sum((rank+1)*next(bid) for rank, bid in enumerate(sorted(hands, key=next)))

w = lambda c,o,d: sum((r+1)*next(b) for r, b in enumerate(sorted((starmap(call,
                  zip((lambda h: (sum(g**2 for g in c(h).values())<<20)+sum(
                  list(o).index(v)<<i*4 for i, v in enumerate(reversed(h))),
                  int), l.split())) for l in d.split("\n")), key=next)))

def jCounter(hand):
    hand = Counter(hand)
    jokers = hand.pop("J", 0)
    hand[next(iter(hand.most_common()), "X")[0]] += jokers
    return hand

part_a = partial(w, Counter, "23456789TJQKA")
part_b = partial(w, jCounter, "J23456789TQKA")

if __name__ == "__main__":
    from aocd import get_data
    print(part_b(get_data(year=2023, day=7)))
