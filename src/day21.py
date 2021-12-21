import functools
import helpers

import itertools
import collections


from dataclasses import dataclass
from dataclasses import replace as copy


@dataclass(frozen=True, eq=True)
class Player:
    name: str
    pos: int
    score: int

    def advance(self, steps):
        new_pos = 1 + (self.pos - 1 + steps) % 10
        new_score = self.score + new_pos
        return copy(self, pos=new_pos, score=new_score)


def main() -> None:
    lines = helpers.read_input()
    print(lines)

    rng = zip(itertools.count(1, 1), itertools.cycle(range(1, 101)))
    p1 = Player("p1", 4, 0)
    p2 = Player("p2", 8, 0)
    roll = []

    while True:
        combo = (p1.score, p2.score)
        roll = list(itertools.islice(rng, 3))
        print(p1)
        p1 = p1.advance(sum(v[1] for v in roll))
        print(p1)

        if p1.score >= 1000:
            break

        combo = (p1.score, p2.score)
        roll = list(itertools.islice(rng, 3))
        p2 = p2.advance(sum(v[1] for v in roll))

        if p2.score >= 1000:
            break
    print(roll)
    print(combo, combo[0] * combo[1])
    print(min(combo) * roll[-1][0])

    p1 = Player("p1", 4, 0)
    p2 = Player("p2", 10, 0)
    print(play_until_21(p1, p2))


@functools.cache
def play_until_21(p1, p2):
    total_wins = [0, 0]
    p1_universe_sums = list(
        sum(t) for t in itertools.product([1, 2, 3], [1, 2, 3], [1, 2, 3])
    )
    for steps in p1_universe_sums:
        p1_copy = copy(p1).advance(steps)
        if p1_copy.score >= 21:
            total_wins[0] += 1
            continue

        p2_universe_sums = list(
            sum(t) for t in itertools.product([1, 2, 3], [1, 2, 3], [1, 2, 3])
        )
        for steps in p2_universe_sums:
            p2_copy = copy(p2).advance(steps)

            if p2_copy.score >= 21:
                total_wins[1] += 1
                continue

            universe_wins = play_until_21(p1_copy, p2_copy)
            total_wins[0] += universe_wins[0]
            total_wins[1] += universe_wins[1]
    return total_wins


main()
