import numpy
import helpers

import itertools
import collections

numpy.set_printoptions(threshold=numpy.inf)
numpy.set_printoptions(linewidth = 1000)

def zero_trim_2d(img):
    p = numpy.where(img != 0)
    return img[min(p[0]) : max(p[0]) + 1, min(p[1]) : max(p[1]) + 1]

def main() -> None:
    lines = helpers.read_input()

    alg = lines[0].replace('#', '1').replace('.', '0')
    print(alg)
    img_lines = lines[2:]
    img = numpy.zeros((len(img_lines), len(img_lines[0])), dtype=int)
    for j in range(len(img_lines)):
        for i in range(len(img_lines[j])):
            img[(i, j)] = img_lines[i][j] == '#' and 1 or 0
    pad_size = 30
    for i in range(2):
        print(img)
        shape = img.shape
        padded_img = numpy.pad(img, 30)
        new_img = numpy.zeros((padded_img.shape[0], padded_img.shape[1]), dtype=int)
        for i in range(padded_img.shape[0]):
            for j in range(padded_img.shape[1]):
                s = ''.join(str(v) for v in helpers.neighbors9_vals(padded_img, i, j))
                n = int(s, 2)
                new_img[i, j] = int(alg[n], 2)
        print(new_img)
        img = new_img
        print(numpy.sum(img == 1))
    img = img[pad_size+1:-pad_size-1,pad_size+1:-pad_size-1]
    print(img)
    print(numpy.sum(img == 1))
    
main()
