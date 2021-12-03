import helpers

import itertools
import collections

def main() -> None:
    lines = helpers.read_input()
    v1, v2 = '', ''
    for i in range(len(lines[0])):
        ones, zeroes = 0, 0
        for line in lines:
            if line[i] == '0':
                zeroes += 1
            else:
                ones += 1
        if ones > zeroes:
            v1 += '1'
            v2 += '0'
        else:
            v1 += '0'
            v2 += '1'
    print(int(v1, 2))
    print(int(v2, 2))
    print(int(v2, 2) * int(v1, 2))

main()
