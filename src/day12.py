import helpers

import itertools
import collections

def can_visit(path, e):
    if e == 'start':
        return False
    if e.upper() == e:
        return True
    if e not in path:
        return True

    lowers = set()
    for p in path:
        if p.lower() == p:
            if p in lowers:
                return False
        lowers.add(p)

    return True

def visit(edges, path):
    ret = [ ]
    for e in edges[path[-1]]:
        if e == 'end':
            ret.append(path + [ e ])
        elif can_visit(path, e):
            ret.extend(visit(edges, path + [ e ]))
    return ret

def main() -> None:
    lines = helpers.read_input()
    edges = collections.defaultdict(set)
    for line in lines:
        e = line.split('-')
        edges[e[0]].add(e[1])
        edges[e[1]].add(e[0])

    paths = set()
    seen = set()
    todo = [ 'start' ]
        
    v = visit(edges, ['start'])
    for p in v:
        print(*p, sep=',')
    print(len(v))

main()
