import helpers

import math
import itertools
import collections

def cost(d):
    d = abs(d)
    return d * (d + 1) // 2

def main() -> None:
    input = helpers.read_input_numbers()
    d = sorted(input)
    for i in range(min(d), max(d) + 1):
        print(i, sum(cost(i - n) for n in d))


main()
