import helpers

import itertools
import collections


def main() -> None:
    lines = helpers.read_input()

    rules = dict()
    for r in lines[2:]:
        k, v = r.split(' -> ')
        rules[k] = v
    
    pairs = collections.defaultdict(int)
    poly = lines[0]
    for a, b in zip(poly[:-1], poly[1:]):
        pairs[a+b] += 1

    for step in range(1, 1000):
        print('pairs', pairs)
        new_pairs = collections.defaultdict(int)
        for p, count in pairs.items():
            if p not in rules:
                new_pairs[p] = count
            else:
                new_pairs[p[0] + rules[p]] += count
                new_pairs[rules[p] + p[1]] += count
        pairs = new_pairs
        print('new_pairs', pairs)
        
        counts = collections.defaultdict(int)
        counts[poly[0]] += 1
        counts[poly[-1]] += 1
        for k, c in pairs.items():
            counts[k[0]] += c
            counts[k[1]] += c
        print('step', step, 'counts', counts)
        print(max(counts.values())//2 - min(counts.values())//2)

main()
