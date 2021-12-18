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
    print('chain!')
    acted = True
    while acted:
        print('pre', render(n))
        acted, n = explode(n)
        if not acted:
            acted, n = split(n)
        print('post', render(n))
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
    return eval(s)

def main() -> None:
    nice_explode([[[[[9,8],1],2],3],4],
         [[[[0,9],2],3],4])

    nice_explode([7,[6,[5,[4,[3,2]]]]],
         [7,[6,[5,[7,0]]]])

    nice_explode([[6,[5,[4,[3,2]]]],1],
         [[6,[5,[7,0]]],3])

    nice_explode([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]],
         [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]])

    nice_explode([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]],
         [[3,[2,[8,0]]],[9,[5,[7,0]]]])

    nice_explode([[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]],
                 [[[[0,7],4],[[7,8],[6,0]]],[8,1]])

    nice_split([10, 1], [[5, 5], 1])

    a = add(parse('[[[[4,3],4],4],[7,[[8,4],9]]]'),
            parse('[1,1]'))
    print(render(a))
    a = chain(a)
    print(render(a))

    print('gooooo')
    lines = helpers.read_input()
    fishes = []
    for f_str in lines:
        fishes.append(parse(f_str))
    f = fishes.pop(0)
    print(render(f))
    while fishes:
        print('add')
        print('  ', render(f))
        print('+ ', render(fishes[0]))
        f = add(f, fishes.pop(0))
        f = chain(f)
        print('= ', render(f))
        print(render(f))
    print(render(f))

    print(magnitude(f))
main()
