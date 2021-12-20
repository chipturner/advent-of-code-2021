import numpy
import helpers

import itertools
import collections

numpy.set_printoptions(threshold=numpy.inf)
numpy.set_printoptions(linewidth=1000)


def zero_trim_2d(img):
    p = numpy.where(img != 0)
    return img[min(p[0]) : max(p[0]) + 1, min(p[1]) : max(p[1]) + 1]


def render_grid(alg, input_grid, i, j):
    output = numpy.zeros((3, 3), dtype=int)
    for delta_i in (-1, 0, 1):
        for delta_j in (-1, 0, 1):
            s = "".join(
                str(v)
                for v in helpers.neighbors9_vals(input_grid, i + delta_i, j + delta_j)
            )
            n = int(s, 2)
            output[1 + delta_i, 1 + delta_j] = int(alg[n], 2)
    return output


def main() -> None:
    lines = helpers.read_input()

    alg = lines[0].replace("#", "1").replace(".", "0")
    print(alg)
    img_lines = lines[2:]
    img = numpy.zeros((len(img_lines), len(img_lines[0])), dtype=int)
    for j in range(len(img_lines)):
        for i in range(len(img_lines[j])):
            img[(i, j)] = img_lines[i][j] == "#" and 1 or 0
    for i in range(25):
        shape = img.shape
        padded_img = numpy.pad(img, 2)
        new_img = numpy.zeros((padded_img.shape[0], padded_img.shape[1]), dtype=int)
        for i in range(padded_img.shape[0]):
            for j in range(padded_img.shape[1]):
                first_pass = render_grid(alg, padded_img, i, j)
                second_pass = render_grid(alg, first_pass, 1, 1)
                new_img[i, j] = second_pass[1, 1]
        img = zero_trim_2d(new_img)
        print(numpy.sum(img == 1))
    print(img)
    print(numpy.sum(img == 1))


main()
