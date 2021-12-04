import numpy
import helpers

import itertools
import collections

def main() -> None:
    orig_data = helpers.read_input_matrix()
    data = orig_data.copy()
    for i in range(len(data[0])):
        transposed = data.transpose()
        m = helpers.most_common_byte(transposed[i])
        data = numpy.array([r for r in data if r[i] == m])
        if len(data) == 1:
            break

    v1 = int(''.join(map(str, data.flatten().tolist())), 2)

    data = orig_data.copy()
    for i in range(len(data[0])):
        transposed = data.transpose()
        m = helpers.most_common_byte(transposed[i]) == 0
        data = numpy.array([r for r in data if r[i] == m])
        if len(data) == 1:
            break
    v2 = int(''.join(map(str, data.flatten().tolist())), 2)
    print(v1 * v2)

main()
