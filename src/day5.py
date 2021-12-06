import helpers

import itertools
import collections
from typing import DefaultDict


def main() -> None:
    lines = helpers.read_input()
    hits: DefaultDict[helpers.Point, int] = collections.defaultdict(int)
    for line in lines:
        p1, p2 = map(helpers.Point.from_str, line.split(" -> "))
        delta = (helpers.cmp(p2.x, p1.x), helpers.cmp(p2.y, p1.y))

        pos = p1
        while pos != p2:
            hits[pos] += 1
            pos = pos + delta
        hits[pos] += 1
    # helpers.print_grid(hits)

    c = 0
    for k, v in hits.items():
        if v > 1:
            c += 1
    print(c)
    helpers.write_grid(hits, "/tmp/foo.png")


main()
