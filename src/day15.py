import helpers

import itertools
import collections

bignum = 1000000000
def main() -> None:
    g = helpers.read_input_digit_grid(int)
    graph = collections.defaultdict(set)
    costs = dict()
    for i in range(g.shape[0]):
        for j in range(g.shape[1]):
            for n in helpers.neighbors(g, i, j):
                graph[(i, j)].add(n)
                graph[n].add((i, j))
            costs[(i, j)] = bignum
    unvisited = list(costs.keys())

    visited = set()
    costs[(0, 0)] = 0
    while unvisited:
        min_cost = min(costs[u] for u in unvisited)
        for n in unvisited:
            if costs[n] == min_cost:
                pos = n
                break
        unvisited.remove(pos)
        for neigh in helpers.neighbors(g, *pos):
            if neigh in visited:
                continue
            costs[neigh] = min(costs[neigh], g[neigh] + costs[pos])
        
        visited.add(pos)
        
    print(costs)
    

main()
