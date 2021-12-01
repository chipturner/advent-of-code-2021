import itertools
import collections
import fileinput

def main() -> None:
    vals = []
    for line in fileinput.input():
        line = line.strip()
        vals.append(int(line.strip()))
    print(vals)
    sums = []
    for idx in range(len(vals) - 2):
        sums.append(sum(vals[idx:idx+3]))
    print("\n".join(str(s) for s in sums))

main()
