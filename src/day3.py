import helpers

import itertools
import collections

def main() -> None:
    orig_lines = helpers.read_input()
    lines = orig_lines
    v1, v2 = '', ''
    oxy_sel = ''
    for i in range(len(lines[0])):
        print(lines)
        ones, zeroes = 0, 0
        for line in lines:
            if line[i] == '0':
                zeroes += 1
            else:
                ones += 1
        mcb = str(int(ones >= zeroes))
        print(mcb)
        lines = [ l for l in lines if l[i] == mcb ]
        oxy_sel = lines[0]
        if len(lines) == 1:
            break
    print(oxy_sel)

    lines = orig_lines
    v1, v2 = '', ''
    co2_sel = ''
    for i in range(len(lines[0])):
        print(lines)
        ones, zeroes = 0, 0
        for line in lines:
            if line[i] == '0':
                zeroes += 1
            else:
                ones += 1
        mcb = str(int(ones < zeroes))
        print(mcb)
        lines = [ l for l in lines if l[i] == mcb ]
        co2_sel = lines[0]
        if len(lines) == 1:
            break
    print(co2_sel)

    print(int(co2_sel, 2) * int(oxy_sel, 2))

main()
