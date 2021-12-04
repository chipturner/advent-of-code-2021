#!usr/bin/python3.9

import fileinput

from typing import List, Tuple, Any
import numpy
import numpy.typing

def read_input() -> List[str]:
    return list(l.strip() for l in fileinput.input())

def read_input_split(sep: str = ' ', nsplit: int = 1) -> List[List[str]]:
    return [l.strip().split(sep, nsplit) for l in read_input()]

def read_input_grid() -> List[List[str]]:
    return list(list(l) for l in read_input())

def read_input_numbers(sep: str = ',') -> List[int]:
    l = read_input()
    assert len(l) == 1
    return [int(s) for s in l[0].split(sep)]

def read_input_matrix() -> Any:
    lines = read_input()
    return numpy.array([ [int(n) for n in l ] for l in lines ])

def most_common_byte(r: numpy.typing.NDArray[numpy.int_]) -> int:
    return int(numpy.sum(r == 1) >= numpy.sum(r == 0))

