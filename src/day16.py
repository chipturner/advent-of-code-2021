import helpers

import itertools
import collections
import operator
import functools

def prod(args):
    return functools.reduce(operator.mul, args)
def eq(args):
    return functools.reduce(operator.eq, args)
def lt(args):
    return functools.reduce(operator.lt, args)
def gt(args):
    return functools.reduce(operator.gt, args)
    
opmap = [ sum, prod, min, max, None, gt, lt, eq]

# packet: 3 bit ver, 3 bit type
# type 4 == literal (5 bits,last starts with 0)
def decode_packet(p):
    ver, type_id = int(p[0:3], 2), int(p[3:6], 2)
    off = 6
    print('decode ver', ver, 'type', type_id, p)

    sub_value = None
    if type_id == 4:
        s = ''
        while p[off] != '0':
            nib = p[off+1:off+5]
            s += nib
            off += 5
        s += p[off+1:off+5]
        literal = int(s, 2)
        print('literal', s, literal)
        off += 5
        sub_value = literal
    else:
        length_type_id = p[off]
        off += 1
        print(type_id)
        print('op is', opmap[type_id])
        if length_type_id == '0':
            nib = p[off:off+15]
            total_length = int(nib, 2)
            off += 15
            end = off + total_length
            print('subpacket length', total_length)
            acc = []
            while off < end:
                consumed, val = decode_packet(p[off:end])
                off += consumed
                acc.append(val)
            print(opmap[type_id], acc)
            sub_value = opmap[type_id](acc)
        else:
            nib = p[off:off+11]
            num_subs = int(nib, 2)
            print('subpacket group', num_subs)
            off += 11
            acc = []
            for i in range(num_subs):
                consumed, val = decode_packet(p[off:])
                off += consumed
                acc.append(val)
            print(opmap[type_id], acc)
            sub_value = opmap[type_id](acc)
    return off, sub_value

def xlate(s):
    return ''.join(f'{int(c, 16):04b}' for c in s)

def main() -> None:
    lines = helpers.read_input()
    if 'A' in lines[0]:
        print(decode_packet(xlate(lines[0])))
    else:
        print(decode_packet(lines[0]))

main()
