import copy
import helpers

import itertools
import collections

class Value:
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return str(self.val)

    def numeric(self):
        return type(self.val) is int

    def __eq__(self, other):
        return self.val == other.val

OPEN = Value('OPEN')
CLOSE = Value('CLOSE')

def parse(s):
    ret = []
    buf = ''
    for c in s:
        if c.isdigit():
            buf += c
            continue
        if buf:
            ret.append(Value(int(buf)))
            buf = ''
        if c == '[':
            ret.append(OPEN)
        elif c == ']':
            ret.append(CLOSE)
        elif c == ',' or c == ' ':
            pass
    if buf:
        ret.append(Value(int(buf)))
    return ret

def explode(l):
    depth = 0
    for idx, val in enumerate(l):
        if val == OPEN:
            depth += 1
        if val == CLOSE:
            depth -= 1
        if depth > 4 and val.numeric() and idx < len(l) and l[idx+1].numeric():
            next_val = l[idx+1]
            #print(l[0:idx-1])
            #print(l[idx+2:])
            for i in range(idx-1, 0, -1):
                if l[i].numeric():
                    l[i].val += val.val
                    break
            for i in range(idx+2, len(l)):
                if l[i].numeric():
                    l[i].val += next_val.val
                    break
            ret = l[0:idx-1] + [Value(0)] + l[idx+3:]
            #print(ret)
            return True, ret
    return False, l

def split(l):
    for idx, val in enumerate(l):
        if val.numeric() and val.val > 9:
            return True, l[:idx] + [ OPEN, Value(val.val //  2), Value((val.val + 1) // 2), CLOSE ] + l[idx+1:]
    return False, l

def render(l):
    ret = ''
    need_comma = True
    for v in l:
        if v == OPEN:
            ret += '['
            need_comma = True
        else:
            if v == CLOSE:
                ret += ']'
            else:
                ret += str(v.val)
            if need_comma:
                ret += ','
    return eval(ret[:-1])

def add(v1, v2):
    return [ OPEN ] + v1 + v2 + [ CLOSE ]

def chain(n):
    acted = True
    while acted:
        acted, n = explode(n)
        if not acted:
            acted, n = split(n)
    return n

def nice_explode(f, expected):
    f = repr(f)
    expected = parse(repr(expected))
    print()
    n = parse(f)
    print(render(n))
    _, n = explode(n)
    print("got:", render(n))
    print("exp:", render(expected))
    print(n == expected)

def nice_split(f, expected):
    f = repr(f)
    expected = parse(repr(expected))
    print()
    n = parse(f)
    print(render(n))
    _, n = split(n)
    print(n)
    print("got:", render(n))
    print("exp:", render(expected))
    print(n == expected)


def m(a, b):
    return 3 * a + 2 * b

def magnitude(f):
    l = repr(render(f))
    s = l.replace('[', 'm(').replace(']', ')')
    print(s)
    eval(s)
    return eval(s)

def main() -> None:
    lines = helpers.read_input()
    magnitudes = []
    fishes = []
    for f_str in lines:
        fishes.append(parse(f_str))
    for i in range(len(fishes)):
        for j in range(len(fishes)):
            if i != j:
                x = add(fishes[i], fishes[j])
                x = chain(copy.deepcopy(x))
                magnitudes.append(magnitude(x))
    print(sorted(magnitudes))
main()
