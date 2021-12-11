import numpy

import helpers

import itertools
import collections

def flash(grid, flash_points, i, j):
    for n in helpers.neighbors8(grid, i, j):
        grid[n] += 1
        if grid[n] >= 10:
            grid[n] = 0
            if not flash_points[n]:
                flash(grid, flash_points, *n)
            flash_points[n] |= True


def main() -> None:
    grid = helpers.read_input_digit_grid(int)
    grid.setflags(write=True)
    print(grid)
    h, w = grid.shape

    total_flashes = 0
    for _ in range(100):
        flash_points = numpy.zeros((h, w), dtype=bool)
        grid += 1
        for i in range(h):
            for j in range(w):
                if grid[i, j] >= 10:
                    grid[i, j] = 0
                    flash_points[i, j] = True
                    flash(grid, flash_points, i, j)

        grid *= (1 - flash_points)
        total_flashes += numpy.sum(flash_points)
        print(grid)
    print(total_flashes)
main()
