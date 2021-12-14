import helpers

import itertools
import collections


def main() -> None:
    lines = helpers.read_input()

    rules = dict()
    for r in lines[2:]:
        k, v = r.split(' -> ')
        rules[k] = v
    

    poly = lines[0]
    step = 1
    for r in rules:
        i = 0
        while i < len(poly):
            m = rules.get(poly[i:i+2], None)
            if m:
                poly = poly[:i+1] + m + poly[i+1:]
                i += 1
            i += 1
        print('step', step, poly)
        step += 1
        if step == 11:
            break
    counts = collections.defaultdict(int)
    for c in poly:
        counts[c] += 1
    print(max(counts.values()) - min(counts.values()))

main()
