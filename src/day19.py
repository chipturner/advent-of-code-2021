import numpy
from math import sin, cos, pi
import helpers

import itertools
import collections

from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class Scanner:
    num: int
    points: List[Tuple[int, int, int]]
    offset: Tuple[int, int, int]
    rotation: Optional[Tuple[int, int]] = None

    def __init__(self, num):
        self.num = int(num)
        self.points = []
        self.offset = (0, 0, 0)


def dist(p1, p2):
    return sum(abs(c1 - c2) for c1, c2 in zip(p1, p2))


def find_12(s1, s2):
    xds = collections.defaultdict(list)
    for p1, p2 in itertools.product(s1.points, s2.points):
        xds[p2[0] - p1[0]].append(pt_diff(p2, p1))
    for xd, xcs in xds.items():
        if len(xcs) < 11:
            continue
        for delta in xcs:
            f2 = fixup(s2, delta)
            ix = set(s1.points).intersection(f2.points)
            if len(ix) >= 11:
                return delta


def rotate(s):
    face_rotations = []
    for x_idx, angle in enumerate((0, pi / 2, pi, 3 * pi / 2)):
        m_x = numpy.array(
            ((1, 0, 0), (0, cos(angle), -sin(angle)), (0, sin(angle), cos(angle))),
            dtype=int,
        )
        face_rotations.append(m_x)
    for y_idx, angle in enumerate((pi / 2, 3 * pi / 2)):
        m_y = numpy.array(
            ((cos(angle), 0, sin(angle)), (0, 1, 0), (-sin(angle), 0, cos(angle))),
            dtype=int,
        )
        face_rotations.append(m_y)
    for z_idx, angle in enumerate((0, pi / 2, pi, 3 * pi / 2)):
        m_z = numpy.array(
            ((cos(angle), -sin(angle), 0), (sin(angle), cos(angle), 0), (0, 0, 1)),
            dtype=int,
        )
        for f_idx, face_rotation in enumerate(face_rotations):
            val = Scanner(s.num)
            val.points = [tuple(p @ m_z @ face_rotation) for p in s.points]
            val.rotation = (f_idx, z_idx)
            yield val


def pt_diff(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2])


def fixup(s, offset):
    ret = Scanner(s.num)
    ret.points = [pt_diff(p, offset) for p in s.points]
    ret.rotation = s.rotation
    ret.offset = offset
    return ret


def main() -> None:
    lines = helpers.read_input()
    scanners = []

    cur_scan = None
    for line in lines:
        if line.startswith("--- scanner "):
            if cur_scan:
                scanners.append(cur_scan)
            cur_scan = Scanner(line[12:].split()[0])
        elif "," in line:
            cur_scan.points.append(tuple([int(v) for v in line.split(",")]))
    scanners.append(cur_scan)

    missing = set(s.num for s in scanners if s.num != 0)
    anchored = {0: scanners[0]}
    while missing:
        print(len(missing), "missing nodes")
        for floater_num in missing:
            print("searching for path to", floater_num)
            floater = scanners[floater_num]
            updated = False
            for rotated_floater in rotate(floater):
                for candidate in anchored.values():
                    offset = find_12(candidate, rotated_floater)
                    if offset:
                        missing.remove(floater.num)
                        anchored_floater = fixup(rotated_floater, offset)
                        anchored[floater.num] = anchored_floater
                        print(
                            f"anchored link: {candidate.num} -> {anchored_floater.num} rot{anchored_floater.rotation} {anchored_floater.offset}"
                        )
                        updated = True
                        break
                if updated:
                    break
            if updated:
                break
    assert len(missing) == 0
    scanners = None

    all_points = set()
    all_points.update(anchored[0].points)
    for scanner in anchored.values():
        from_id, to_id = anchored[0].num, scanner.num
        if from_id == to_id:
            continue
        fixed = anchored[to_id]
        offset = fixed.offset
        print(f"fix for {from_id} to {to_id} is {fixed.offset}")
        all_points.update(fixed.points)
    print(len(all_points))

    dists = []
    for p1 in anchored.values():
        for p2 in anchored.values():
            dists.append(dist(p1.offset, p2.offset))
    print(max(dists))


main()
