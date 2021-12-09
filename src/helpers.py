#!usr/bin/python3.9

from __future__ import annotations

import fileinput
from dataclasses import dataclass

from typing import List, Tuple, Any, Dict, Sequence, TypeVar
import numbers
import numpy
import numpy.typing

import PIL.Image, PIL.ImageDraw


def read_input() -> List[str]:
    return list(l.strip() for l in fileinput.input())


def read_input_split(sep: str = " ", nsplit: int = 1) -> List[List[str]]:
    return [l.strip().split(sep, nsplit) for l in read_input()]


def read_input_grid() -> numpy.typing.NDArray[numpy.str_]:
    return numpy.array(list(list(l) for l in read_input()))

def read_input_grid_int() -> numpy.typing.NDArray[numpy.int_]:
    return numpy.array(list(list(int(i) for i in l) for l in read_input()))


def read_input_numbers(sep: str = ",") -> List[int]:
    l = read_input()
    assert len(l) == 1
    return [int(s) for s in l[0].split(sep)]


def read_input_matrix() -> Any:
    lines = read_input()
    return numpy.array([[int(n) for n in l] for l in lines])


def most_common_byte(r: numpy.typing.NDArray[numpy.int_]) -> int:
    return int(numpy.sum(r == 1) >= numpy.sum(r == 0))


# Goofy replacement since cmp was removed in python3 (!)
def cmp(a: int, b: int) -> int:
    return (a > b) - (a < b)


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    @staticmethod
    def from_str(s: str) -> Point:
        return Point(*map(int, s.split(",")))

    def __add__(self, other: Tuple[int, int]) -> Point:
        x, y = other
        return Point(self.x + x, self.y + y)


def print_grid(g: Dict[Point, Any]) -> None:
    min_i = min(p.x for p in g.keys())
    max_i = max(p.x for p in g.keys())
    min_j = min(p.y for p in g.keys())
    max_j = max(p.y for p in g.keys())
    for j in range(min_i, max_i + 1):
        for i in range(min_j, max_j + 1):
            print(g[Point(i, j)] or ".", end="")
        print()


def write_grid(grid: Dict[Point, int], path: str) -> None:
    img_size = 3000
    min_i = min(p.x for p in grid.keys())
    max_i = max(p.x for p in grid.keys())
    min_j = min(p.y for p in grid.keys())
    max_j = max(p.y for p in grid.keys())
    x_range, y_range = max_i - min_i, max_j - min_j
    square_range = max(x_range, y_range)
    scale = img_size / square_range
    max_fill = max(grid.values())

    img = PIL.Image.new("RGB", (img_size, img_size))
    draw = PIL.ImageDraw.Draw(img)
    for pt, count in grid.items():
        r, g, b = (count * int(255 / max_fill),) * 3
        if count == max_fill:
            print(pt, count, r)
            (r, g, b) = (255, 0, 0)
        draw.rectangle(
            (scale * pt.x, scale * pt.y, scale * (pt.x + 1), scale * (pt.y + 1)),
            fill=(r, g, b),
        )
    img.save(path)
