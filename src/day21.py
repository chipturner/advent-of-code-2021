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
    for p1_start in range(10):
        for p2_start in range(10):
            p1 = Player("p1", p1_start + 1, 0)
            p2 = Player("p2", p2_start + 1, 0)
            counts = play_until_21(p1, p2)
            print(f'Start: {p1_start+1}, {p2_start+1} -> {counts} {counts[0]/(counts[0]+counts[1]):.2f}')


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
