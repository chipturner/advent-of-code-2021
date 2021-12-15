import numpy
import helpers

import itertools
import collections
import heapq

bignum = 1000000000
def main() -> None:
    g = helpers.read_input_digit_grid(int)
    base_graph = helpers.read_input_digit_grid(int)
    g = numpy.zeros((base_graph.shape[0] * 5, base_graph.shape[1] * 5), dtype=int)
    numpy.set_printoptions(threshold=10000)
    numpy.set_printoptions(linewidth=numpy.inf)
    for m in range(5):
        for n in range(5):
            g[m * base_graph.shape[0]:(m+1) * base_graph.shape[0], n * base_graph.shape[0]:(n+1) * base_graph.shape[0]] = (base_graph + m + n + 8) % 9 + 1

    graph = collections.defaultdict(set)
    costs = dict()
    for i in range(g.shape[0]):
        for j in range(g.shape[1]):
            for n in helpers.neighbors(g, i, j):
                graph[(i, j)].add(n)
                graph[n].add((i, j))
            costs[(i, j)] = bignum

    visited = set()
    costs[(0, 0)] = 0
    pq = []
    pq_seen = set()
    heapq.heappush(pq, (0, (0, 0)))
    while pq:
        cost, pos = heapq.heappop(pq)
        for neigh in helpers.neighbors(g, *pos):
            if neigh in visited:
                continue
            costs[neigh] = min(costs[neigh], g[neigh] + costs[pos])
            entry = (costs[neigh], neigh)
            if entry not in pq_seen:
                pq_seen.add(entry)
                heapq.heappush(pq, entry)
        
        visited.add(pos)
        
    print(costs)
    

main()
