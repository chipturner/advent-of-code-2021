import helpers

import itertools
import collections


def main() -> None:
    lines = helpers.read_input()
    print(lines)

    rng = zip(itertools.count(1, 1), itertools.cycle(range(1, 101)))
    p1_pos, p2_pos = 4, 10
    p1_score, p2_score = 0, 0
    combo = 0
    winner_score = 0
    roll = []
    
    while True:
        combo = (p1_score, p2_score)
        roll = list(itertools.islice(rng, 3))
        p1_pos += sum(v[1] for v in roll)
        p1_pos = 1 + (p1_pos - 1) % 10
        p1_score += p1_pos

        if p1_score >= 1000:
            break

        combo = (p1_score, p2_score)
        roll = list(itertools.islice(rng, 3))
        p2_pos += sum(v[1] for v in roll)
        p2_pos = 1 + (p2_pos - 1) % 10
        p2_score += p2_pos

        if p2_score >= 1000:
            break
    print(roll)
    print(combo, combo[0] * combo[1])
    print(min(combo) * roll[-1][0])

main()
