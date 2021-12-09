import numpy
import helpers

import copy

import itertools
import collections


def is_match(i, j, grid):
    if i < 0 or j < 0:
        return False
    for x, y in ((i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j)):
        try:
            if grid[i][j] >= grid[x][y]:
                return False
        except IndexError:
            pass
    return True


def valley_size(val, i, j, grid):
    if i < 0 or j < 0:
        return 0
    if grid[i][j] >= 9:
        return 0
    grid[i][j] = 10
    for x, y in ((i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j)):
        try:
            if grid[x][y] < 9 and grid[x][y] >= val:
                valley_size(grid[x][y], x, y, grid)
        except IndexError:
            pass
    return numpy.sum(grid == 10)


def main() -> None:
    lines = helpers.read_input_grid_int()

    h = len(lines[0])
    w = len(lines)

    valleys = []
    for i in range(w):
        for j in range(h):
            if is_match(i, j, lines):
                valleys.append((i, j))

    vals = []
    for i, j in valleys:
        grid = copy.deepcopy(lines)
        vals.append(valley_size(grid[i][j], i, j, grid))
    vals = sorted(vals)[-3:]
    print(vals[0] * vals[1] * vals[2])


main()
