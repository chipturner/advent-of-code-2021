#!usr/bin/python3.9

from __future__ import annotations

from enum import Enum
import io
import functools
import fileinput
import operator
from dataclasses import dataclass

from typing import (
    List,
    Tuple,
    Any,
    Dict,
    Sequence,
    TypeVar,
    Callable,
    Iterable,
    Optional,
    TextIO,
)
import numbers
import numpy
import numpy.typing

import PIL.Image, PIL.ImageDraw


# list of lines
def read_input() -> List[str]:
    return list(l.strip() for l in fileinput.input())


# list of lists of lines split by delimiter
def read_input_split(sep: str = " ", nsplit: int = 1) -> List[List[str]]:
    return [l.strip().split(sep, nsplit) for l in read_input()]


T = TypeVar("T", bound=numpy.generic)

# grid of densly packed digits like '12139' etc
def read_input_digit_grid(conv: Callable[[str], T]) -> numpy.typing.NDArray[T]:
    ret = numpy.array(list(list(conv(i) for i in l) for l in read_input()))
    ret.setflags(write=False)
    return ret


# single line of separated numbers
def read_input_numbers(sep: str = ",") -> List[int]:
    l = read_input()
    assert len(l) == 1
    return [int(s) for s in l[0].split(sep)]


NumericGrid = numpy.typing.NDArray[numpy.int_]


def most_common_byte(r: NumericGrid) -> int:
    return int(numpy.sum(r == 1) >= numpy.sum(r == 0))


def neighbors(grid: NumericGrid, i: int, j: int) -> Iterable[Tuple[int, int]]:
    h, w = grid.shape
    for pos in ((i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j)):
        if pos[0] < 0 or pos[1] < 0 or pos[0] >= h or pos[1] >= w:
            continue
        yield pos


def neighbors8(grid: NumericGrid, i: int, j: int) -> Iterable[Tuple[int, int]]:
    h, w = grid.shape
    for pos in (
        (i, j + 1),
        (i, j - 1),
        (i + 1, j),
        (i - 1, j),
        (i + 1, j + 1),
        (i - 1, j - 1),
        (i + 1, j - 1),
        (i - 1, j + 1),
    ):
        if pos[0] < 0 or pos[1] < 0 or pos[0] >= h or pos[1] >= w:
            continue
        yield pos


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
    for j in range(min_j, max_j + 1):
        for i in range(min_i, max_i + 1):
            print(g.get(Point(i, j), "."), end="")
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


class BitsOperator(Enum):
    SUM = 0
    PRODUCT = 1
    MIN = 2
    MAX = 3
    LITERAL = 4
    GT = 5
    LT = 6
    EQ = 7


def prod(args: List[int]) -> int:
    return functools.reduce(operator.mul, args)


def eq(args: List[int]) -> int:
    return functools.reduce(operator.eq, args)


def lt(args: List[int]) -> int:
    return functools.reduce(operator.lt, args)


def gt(args: List[int]) -> int:
    return functools.reduce(operator.gt, args)


def fail(args: List[int]) -> int:
    return 0


opmap: List[Callable[[List[int]], int]] = [sum, prod, min, max, fail, gt, lt, eq]


@dataclass
class BitsPacket:
    version: int
    type_id: BitsOperator
    children: List[BitsPacket]
    literal_value: Optional[int]

    def __init__(self, version: int, type_id: int):
        self.version = version
        self.type_id = BitsOperator(type_id)
        self.children = []
        self.literal_value = None

    def eval(self) -> int:
        if self.type_id == BitsOperator.LITERAL:
            assert self.literal_value is not None
            return self.literal_value
        else:
            results = [c.eval() for c in self.children]
            return opmap[self.type_id.value](results)

    def print(self, indent: str = "") -> None:
        if self.type_id == BitsOperator.LITERAL:
            print(
                f"{indent}BitsPacket(ver={self.version}, type-{self.type_id}, val={self.literal_value})"
            )
        else:
            print(f"{indent}BitsPacket(ver={self.version}, type-{self.type_id})")
            for c in self.children:
                c.print(indent + "  ")


def decode_packet(p: TextIO) -> BitsPacket:
    ver, type_id = int(p.read(3), 2), int(p.read(3), 2)
    print("decode ver", ver, "type", type_id, p)

    packet = BitsPacket(ver, type_id)

    sub_value = None
    if type_id == 4:
        s = ""
        while p.read(1) != "0":
            nib = p.read(4)
            s += nib
        s += p.read(4)
        literal = int(s, 2)
        print("literal", s, literal)
        sub_value = literal
        packet.literal_value = literal
    else:
        length_type_id = p.read(1)
        print(type_id)
        print("op is", type_id)
        if length_type_id == "0":
            nib = p.read(15)
            total_length = int(nib, 2)
            print("subpacket length", total_length)
            p = io.StringIO(p.read(total_length))
            acc = []
            while p.tell() < total_length:
                val = decode_packet(p)
                acc.append(val)
            packet.children = acc
        else:
            nib = p.read(11)
            num_subs = int(nib, 2)
            print("subpacket group", num_subs)
            acc = []
            for i in range(num_subs):
                val = decode_packet(p)
                acc.append(val)
            packet.children = acc
    return packet
