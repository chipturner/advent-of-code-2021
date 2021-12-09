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


def valley_size(grid: helpers.NumericGrid, val: int, i: int, j: int) -> int:
    if grid[i, j] >= 9:
        return 0
    grid[i, j] = 10
    for x, y in helpers.neighbors(grid, i, j):
        try:
            if grid[x, y] < 9 and grid[x, y] >= val:
                valley_size(grid, grid[x, y], x, y)
        except IndexError:
            pass
    return int(numpy.sum(grid == 10))


def main() -> None:
    grid = helpers.read_input_grid(numpy.int_)
    w, h = grid.shape

    valleys = []
    for i in range(w):
        for j in range(h):
            if is_match(grid, i, j):
                valleys.append((i, j))

    vals = []
    for i, j in valleys:
        vals.append(valley_size(grid.copy(), grid[i, j], i, j))
    vals = sorted(vals)[-3:]
    print(vals[0] * vals[1] * vals[2])


main()
