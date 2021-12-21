import helpers

import itertools
import collections


from dataclasses import dataclass


@dataclass
class Player:
    pos: int
    score: int

    def advance(self, steps):
        self.pos = 1 + (self.pos - 1 + steps) % 10
        self.score += self.pos


def main() -> None:
    lines = helpers.read_input()
    print(lines)

    rng = zip(itertools.count(1, 1), itertools.cycle(range(1, 101)))
    p1 = Player(4, 0)
    p2 = Player(8, 0)
    roll = []

    while True:
        combo = (p1.score, p2.score)
        roll = list(itertools.islice(rng, 3))
        p1.advance(sum(v[1] for v in roll))

        if p1.score >= 1000:
            break

        combo = (p1.score, p2.score)
        roll = list(itertools.islice(rng, 3))
        p2.advance(sum(v[1] for v in roll))

        if p2.score >= 1000:
            break
    print(roll)
    print(combo, combo[0] * combo[1])
    print(min(combo) * roll[-1][0])


main()
