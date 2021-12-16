import helpers

import itertools
import collections
import operator
import functools
import io

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
    ver, type_id = int(p.read(3), 2), int(p.read(3), 2)
    print('decode ver', ver, 'type', type_id, p)

    sub_value = None
    if type_id == 4:
        s = ''
        while p.read(1) != '0':
            nib = p.read(4)
            s += nib
        s += p.read(4)
        literal = int(s, 2)
        print('literal', s, literal)
        sub_value = literal
    else:
        length_type_id = p.read(1)
        print(type_id)
        print('op is', opmap[type_id])
        if length_type_id == '0':
            nib = p.read(15)
            total_length = int(nib, 2)
            print('subpacket length', total_length)
            p = io.StringIO(p.read(total_length))
            acc = []
            while p.tell() < total_length:
                val = decode_packet(p)
                acc.append(val)
            print(opmap[type_id], acc)
            sub_value = opmap[type_id](acc)
        else:
            nib = p.read(11)
            num_subs = int(nib, 2)
            print('subpacket group', num_subs)
            acc = []
            for i in range(num_subs):
                val = decode_packet(p)
                acc.append(val)
            print(opmap[type_id], acc)
            sub_value = opmap[type_id](acc)
    return sub_value

def main() -> None:
    lines = helpers.read_input()
    if 'A' in lines[0]:
        s = bin(int(lines[0], 16))[2:]
    else:
        s = lines[0]
    print(decode_packet(io.StringIO(s)))

main()
