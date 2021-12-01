import itertools
import more_itertools
import collections
import fileinput

def main() -> None:
    vals = []
    for line in fileinput.input():
        line = line.strip()
        vals.append(int(line.strip()))
    print(vals)
    sums = [ sum(v) for v in more_itertools.windowed(vals, 1) ]
    incs = sum(v0 < v1 for (v0, v1) in zip(sums[:-1], sums[1:]))
    print(incs)

main()
