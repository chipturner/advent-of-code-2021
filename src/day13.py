import helpers

import itertools
import collections


def main() -> None:
    lines = helpers.read_input()
    grid = dict()
    folds = list()
    for line in lines:
        print(line)
        if not line:
            continue
        if line.startswith('fold along'):
            f = line[11:]
            folds.append(f.split('='))
        else:
            x, y = map(int, line.split(','))
            grid[helpers.Point(x, y)] = '#'

    print(grid)
    for fold in folds:
        print()
        helpers.print_grid(grid)
        print()
        max_i = max(p.x for p in grid.keys())+1
        max_j = max(p.y for p in grid.keys())+1
        new_grid = dict()
        seam = int(fold[1])
        if fold[0] == 'y':
            for i in range(max_i):
                grid[helpers.Point(i, seam)] = '-'
            helpers.print_grid(grid)
            for i in range(max_i):
                for j in range(seam):
                    p = helpers.Point(i, j)
                    flip_p = helpers.Point(i, 2 * seam - j)
                    new_grid[p] = '.'
                    if grid.get(p, '.') == '#' or grid.get(flip_p, '.') == '#':
                        new_grid[p] = '#'
            grid = new_grid
        elif fold[0] == 'x':
            for j in range(max_j):
                grid[helpers.Point(seam, j)] = '|'
            helpers.print_grid(grid)
            for i in range(seam):
                for j in range(max_j):
                    p = helpers.Point(i, j)
                    flip_p = helpers.Point(2 * seam - i, j)
                    new_grid[p] = '.'
                    if grid.get(p, '.') == '#' or grid.get(flip_p, '.') == '#':
                        new_grid[p] = '#'
            grid = new_grid

    helpers.print_grid(grid)
    print(sum(1 for v in grid.values() if v == '#'))

main()
