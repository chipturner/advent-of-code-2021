import helpers

import itertools
import collections
import io

# packet: 3 bit ver, 3 bit type
# type 4 == literal (5 bits,last starts with 0)
def decode_packet(p):
    ver, type_id = int(p.read(3), 2), int(p.read(3), 2)
    print("decode ver", ver, "type", type_id, p)

    packet = helpers.BitsPacket(ver, type_id)

    sub_value = None
    if type_id == 4:
        s = ""
        while p.read(1) != "0":
            nib = p.read(4)
            s += nib
        s += p.read(4)
        literal = int(s, 2)
        print("literal", s, literal)
        sub_value = literal
        packet.literal_value = literal
    else:
        length_type_id = p.read(1)
        packet.operator = type_id
        print(type_id)
        print("op is", type_id)
        if length_type_id == "0":
            nib = p.read(15)
            total_length = int(nib, 2)
            print("subpacket length", total_length)
            p = io.StringIO(p.read(total_length))
            acc = []
            while p.tell() < total_length:
                val = decode_packet(p)
                acc.append(val)
            packet.children = acc
        else:
            nib = p.read(11)
            num_subs = int(nib, 2)
            print("subpacket group", num_subs)
            acc = []
            for i in range(num_subs):
                val = decode_packet(p)
                acc.append(val)
            packet.children = acc
    return packet


def main() -> None:
    lines = helpers.read_input()
    if "A" in lines[0]:
        s = bin(int(lines[0], 16))[2:]
    else:
        s = lines[0]
    packet = decode_packet(io.StringIO(s))
    packet.print()
    print(packet.eval())


main()
