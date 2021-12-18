import helpers

from typing import Iterable, Tuple
import itertools
import collections


def sign(n: int) -> int:
    if n < 0:
        return -1
    if n > 0:
        return 1
    return 0


def trajectory(xv: int, yv: int) -> Iterable[Tuple[int, int, int]]:
    x, y = 0, 0
    step = 0
    while True:
        x += xv
        y += yv
        xv += -sign(xv)
        yv -= 1
        step += 1
        yield step, x, y


def inside_box(min_x: int, x: int, max_x: int, min_y: int, y: int, max_y: int) -> bool:
    return (min_x <= x <= max_x) and (min_y <= y <= max_y)


def viable(
    xv: int, min_x: int, x: int, max_x: int, yv: int, min_y: int, y: int, max_y: int
) -> bool:
    if xv == 0 and not (min_x <= x <= max_x):
        return False
    if x > max_x:
        return False
    if y < min_y:
        return False
    return True


def main() -> None:
    min_x, max_x = 20, 30
    min_y, max_y = -10, -5

    min_x, max_x = 143, 177
    min_y, max_y = -106, -71

    candidates = set()
    for xv in range(0, 1000):
        for yv in range(-1000, 1000):
            for step, x, y in trajectory(xv, yv):
                if not viable(xv, min_x, x, max_x, yv, min_y, y, max_y):
                    break
                if inside_box(min_x, x, max_x, min_y, y, max_y):
                    candidates.add((step, x, y))
    print(candidates)
    print(len(candidates))


main()
