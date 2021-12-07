import helpers

import math
import itertools
import collections


def main() -> None:
    input = helpers.read_input_numbers()
    d = sorted(input)
    for i in d:
        print(i, sum(abs(i - n) for n in d))


main()
