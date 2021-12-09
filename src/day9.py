import numpy
import helpers

import copy

import itertools
import collections


def is_match(grid: helpers.NumericGrid, i: int, j: int) -> bool:
    if i < 0 or j < 0:
        return False
    for x, y in helpers.neighbors(grid, i, j):
        if grid[i, j] >= grid[x, y]:
            return False
    return True


def valley_size(grid: helpers.NumericGrid, i: int, j: int) -> int:
    seen = set()
    todo = [(i, j)]

    size = 0
    while todo:
        p = todo.pop(0)
        if p in seen or grid[p] == 9:
            continue
        size += 1
        seen.add(p)
        for neighbor in helpers.neighbors(grid, *p):
            todo.append(neighbor)
    return size


def main() -> None:
    grid = helpers.read_input_digit_grid(numpy.int_)
    w, h = grid.shape

    valleys = []
    for i in range(w):
        for j in range(h):
            if is_match(grid, i, j):
                valleys.append((i, j))

    vals = []
    for i, j in valleys:
        vals.append(valley_size(grid, i, j))
    vals = sorted(vals)[-3:]
    print(vals[0] * vals[1] * vals[2])


main()
