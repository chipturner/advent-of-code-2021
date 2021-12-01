import itertools
import collections
import fileinput

def main() -> None:
    for line in fileinput.input():
        line = line.strip()
        print(line)

main()