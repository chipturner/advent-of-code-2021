import helpers

import itertools
import collections

def visit(edges, forbidden, path):
    if path[-1] == 'end':
        return [ path ]
    ret = [ ]
    for e in edges[path[-1]]:
        if e not in forbidden:
            if e.lower() == e:
                ret.extend(visit(edges, forbidden.union({e}), path + [ e ]))
            else:
                ret.extend(visit(edges, forbidden, path + [ e ]))
    return ret

def main() -> None:
    lines = helpers.read_input()
    edges = collections.defaultdict(set)
    for line in lines:
        e = line.split('-')
        edges[e[0]].add(e[1])
        edges[e[1]].add(e[0])
    print(edges)

    paths = set()
    seen = set()
    todo = [ 'start' ]
        
    v = visit(edges, {'start'}, ['start'])
    print(len(v))
    print(v)

main()
