import helpers

import itertools
import collections

def main() -> None:
    z, x, aim = 0, 0, 0
    lines = helpers.read_input_split(' ', 2)
    for cmd, v in lines:
        n = int(v)
        if cmd == 'up':
            aim -= n
        elif cmd == 'down':
            aim += n
        else:
            x += n
            z += n * aim
        print(f"z={z}, x={x}")
    print(x*z)
        

main()
