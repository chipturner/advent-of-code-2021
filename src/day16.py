import helpers

import itertools
import collections

# packet: 3 bit ver, 3 bit type
# type 4 == literal (5 bits,last starts with 0)
vsum = 0
def decode_packet(p):
    ver, type_id = int(p[0:3], 2), int(p[3:6], 2)
    global vsum
    vsum += ver
    off = 6
    print('decode ver', ver, 'type', type_id, p)
    
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
    else:
        length_type_id = p[off]
        off += 1
        if length_type_id == '0':
            nib = p[off:off+15]
            total_length = int(nib, 2)
            off += 15
            end = off + total_length
            print('subpacket length', total_length)
            while off < end:
                off += decode_packet(p[off:end])
        else:
            nib = p[off:off+11]
            num_subs = int(nib, 2)
            print('subpacket group', num_subs)
            off += 11
            for i in range(num_subs):
                off += decode_packet(p[off:])
    return off

def xlate(s):
    return ''.join(f'{int(c, 16):04b}' for c in s)

def main() -> None:
    lines = helpers.read_input()
    if 'A' in lines[0]:
        decode_packet(xlate(lines[0]))
    else:
        decode_packet(lines[0])
    global vsum
    print(vsum)

main()
