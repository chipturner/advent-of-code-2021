import helpers

import itertools
import collections

def main() -> None:
    lines = helpers.read_input()
    hits = collections.defaultdict(int)
    for line in lines:
        p1, p2 = line.split(' -> ')
        p1x, p1y = map(int, p1.split(','))
        p2x, p2y = map(int, p2.split(','))

        delta = [0, 0]
        end = [p1x, p1y]
        pos = [p2x, p2y]
        print('seg', pos, end)
        if p1x < p2x:
            delta[0] = -1
        elif p1x > p2x:
            delta[0] = 1
        if p1y < p2y:
            delta[1] = -1
        elif p1y > p2y:
            delta[1] = 1
        print('delta', delta)

        while tuple(pos) != tuple(end):
            print(pos, end)
            hits[tuple(pos)] += 1
            pos[0] += delta[0]
            pos[1] += delta[1]
        hits[tuple(end)] += 1
    for j in range(10):
        for i in range(10):
            print(hits[(i, j)] or '.', end='')
        print()
    c = 0
    for k, v in hits.items():
        if v > 1:
            print(k, v)
            c += 1
    print(c)

main()
