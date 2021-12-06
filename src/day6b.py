import helpers

import itertools
import functools
import collections

from dataclasses import dataclass

@dataclass
class Fish:
    span: int

@functools.cache
def new_fish_in_days(days):
    ret = 0
    for i in range(days):
        if i % 7 == 0:
            ret += 1
            ret += new_fish_in_days(days - i - 9)
    return ret
    
def main() -> None:
    lines = helpers.read_input()
    fishes = [ Fish(int(s)) for s in lines[0].split()[-1].split(',') ]
    print(fishes)
    total_fish = len(fishes)
    for f in fishes:
        n = new_fish_in_days(256 - f.span)
        print(f"fish {f} makes {n} fishes")
        total_fish += n
    print(total_fish)

main()
