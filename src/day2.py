import itertools
import collections
import fileinput


def main() -> None:
    z, x, aim = 0, 0, 0
    for line in fileinput.input():
        line = line.strip().split()
        n = int(line[1])
        if line[0] == 'up':
            aim -= n
        elif line[0] == 'down':
            aim += n
        else:
            x += n
            z += n * aim
        print(f"z={z}, x={x}")
    print(x*z)
        

main()
