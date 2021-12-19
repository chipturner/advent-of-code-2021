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
    rotation: Optional[Tuple[int, int]] = None
    def __init__(self, num):
        self.num = int(num)
        self.points = []

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
#            print('delta', xd, delta)
#            print('  ', s2.points)
            f2 = fixup(s2, delta)
#            print('  ', f2.points)
            ix = set(s1.points).intersection(f2.points)
#            print('ix', ix)
            if len(ix) >= 11:
                return delta, len(ix)
        

def rotate(s):
    face_rotations = []
    for x_idx, angle in enumerate((0, pi/2, pi, 3 * pi / 2)):
        m_x = numpy.array(((1, 0, 0),
                           (0, cos(angle), -sin(angle)),
                           (0, sin(angle), cos(angle))), dtype=int)
        face_rotations.append(m_x)
    for y_idx, angle in enumerate((pi/2, 3 * pi / 2)):
        m_y = numpy.array(((cos(angle), 0, sin(angle)),
                           (0, 1, 0),
                           (-sin(angle), 0, cos(angle))), dtype=int)
        face_rotations.append(m_y)
    for z_idx, angle in enumerate((0, pi/2, pi, 3 * pi / 2)):
        m_z = numpy.array(((cos(angle),-sin(angle), 0),
                           (sin(angle), cos(angle), 0),
                            (0, 0, 1)), dtype=int)
        for f_idx, face_rotation in enumerate(face_rotations):
            val = Scanner(s.num)
            val.points = [ tuple(p @ m_z @ face_rotation) for p in s.points ]
            val.rotation = (f_idx, z_idx)
            yield val

def pt_diff(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2])

def neg(pt):
    return -pt[0], -pt[1], -pt[2]

def fixup(s, pt):
    ret = Scanner(s.num)
    ret.points = [ pt_diff(p, pt) for p in s.points ]
    ret.rotation = s.rotation
    return ret
    
def find_path(g, a, b):
    todo = [ (a, []) ]
    while todo:
        n, path = todo.pop(0)
        if n == b:
            return path + [ b ]
        for p in g[n]:
            todo.append((p, path + [ n ]))
    return None

def combine_path(path, links):
    ret = [0,0,0]
    for idx in range(len(path) - 1):
        diff, _ = links[path[idx]][path[idx+1]]
        for i in (0, 1, 2):
            ret[i] += diff[i]
    return tuple(ret)

def main() -> None:
    lines = helpers.read_input()
    scanners = []

    cur_scan = None
    for line in lines:
        if line.startswith('--- scanner '):
            if cur_scan:
                scanners.append(cur_scan)
            cur_scan = Scanner(line[12:].split()[0])
        elif ',' in line:
            cur_scan.points.append(tuple([int(v) for v in line.split(',')]))
    scanners.append(cur_scan)

    links = collections.defaultdict(dict)
    rotated = { s.num: s for s in scanners }

    horizon = [ 0 ]
    seen = set()
    while horizon:
        nxt = scanners[horizon.pop(0)]
        seen.add(nxt.num)
        print('springing from', nxt.num)
        for other in scanners:
            if other.num == nxt.num or other.num in seen:
                continue
            for candidate in rotate(other):
                refs = find_12(nxt, candidate)
                if refs:
                    horizon.append(candidate.num)
                    links[nxt.num][candidate.num] = (refs[0], candidate)
                    scanners[candidate.num] = candidate
                    print(f'link: {nxt.num} {candidate.num} rot{candidate.rotation} {refs}')
                    break
    missing = []
    for s in scanners[1:]:
        if s.num not in links[0]:
            missing.append((0, s.num))
    print('missing', missing)

    for m in missing:
        path = find_path(links, m[0], m[1])
        new_path = combine_path(path, links)
        links[m[0]][m[1]] = new_path, None

    all_points = set()
    all_points.update(scanners[0].points)
    scanner_positions = dict()
    for scanner in scanners[1:]:
        from_id, to_id = scanners[0].num, scanner.num
        if from_id == to_id:
            continue
        delta, _ = links[from_id][to_id]
        fixed = fixup(scanner, delta)
        scanner_positions[scanner.num] = delta
        print(f'fix for {from_id} to {to_id} is {delta}')
        print(from_id, to_id, fixed.points)
        all_points.update(fixed.points)
    print(len(all_points))

    dists = []
    for p1 in scanner_positions.values():
        for p2 in scanner_positions.values():
            dists.append(dist(p1, p2))
    print(max(dists))

main()
