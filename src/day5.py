import helpers

import itertools
import collections

def main() -> None:
    lines = helpers.read_input()
    hits = collections.defaultdict(int)
    for line in lines:
        p1, p2 = map(helpers.Point.from_str, line.split(' -> '))
        delta = [0, 0]
        print('seq  ', p1, p2)
        if p1.x < p2.x:
            delta[0] = 1
        elif p1.x > p2.x:
            delta[0] = -1
        if p1.y < p2.y:
            delta[1] = 1
        elif p1.y > p2.y:
            delta[1] = -1
        delta = helpers.Point(*delta)
        print('delta', delta)

        pos = p1
        while pos != p2:
            hits[pos] += 1
            pos = pos + delta
        hits[pos] += 1
    helpers.print_grid(hits)

    c = 0
    for k, v in hits.items():
        if v > 1:
            c += 1
    print(c)

main()
