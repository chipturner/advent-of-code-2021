import itertools
import collections
import fileinput

def main() -> None:
    lines = list(l.strip() for l in fileinput.input())
    print(lines)

main()
