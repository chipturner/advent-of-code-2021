import helpers

import itertools
import collections

from dataclasses import dataclass

@dataclass
class Fish:
    span: int

def main() -> None:
    lines = helpers.read_input()
    fishes = [ Fish(int(s)) for s in lines[0].split()[-1].split(',')]
    print(fishes)
    for d in range(256):
        msg = ','.join(str(f.span) for f in fishes)
        print(f"After {d:2} days: {msg}")
        new_fishes = []
        for fish in fishes:
            fish.span -= 1
            if fish.span == -1:
                fish.span = 6
                new_fishes.append(Fish(8))
        fishes.extend(new_fishes)
    print(f"Total fish: {len(fishes)}")

main()
