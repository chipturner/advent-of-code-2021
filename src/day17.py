import numpy
import helpers

import itertools
import collections

def x_candidates(xv, min_x, max_x):
    pos = 0
    step = 0
    while step < 1000:
        step += 1
        pos += xv
        xv += -numpy.sign(xv)
        if min_x <= pos <= max_x:
            yield step
        if pos > max_x:
            break
        if xv == 0 and pos < min_x:
            break


def y_candidates(yv, min_y, max_y):
    pos = 0
    step = 0
    while True:
        step += 1
        pos += yv
        yv -= 1
        if min_y <= pos <= max_y:
            yield step
        if pos < min_y:
            return

def max_ypos(step, yv, min_y, max_y):
    max_seen_y = 0
    pos = 0
    for i in range(1, step):
        max_seen_y = max(max_seen_y, pos)
        pos += yv
        yv -= 1
        if pos < min_y:
            break
    return max_seen_y

def main() -> None:
    # s = 'target area: x=20..30, y=-10..-5'
    # s = 'target area: x=143..177, y=-106..-71'
    min_x, max_x = 20, 30
    min_y, max_y = -10, -5
    min_x, max_x = 143, 177
    min_y, max_y = -106, -71


    y_step_hits = collections.defaultdict(set)
    for yv in range(0, 1000):
        for step in y_candidates(yv, min_y, max_y):
            y_step_hits[step].add(yv)

    x_step_hits = collections.defaultdict(set)
    for xv in range(0, max_x + 5):
        for step in x_candidates(xv, min_x, max_x):
            x_step_hits[step].add(xv)

    candidates = []
    for s, yvs in y_step_hits.items():
        xvs = x_step_hits.get(s, set())
        print(s, xvs, yvs)
        for xv, yv in itertools.product(xvs, yvs):
            candidates.append(max_ypos(s, yv, min_y, max_y))
    print(candidates)


main()
