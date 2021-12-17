import helpers

import itertools
import collections
import io


def main() -> None:
    lines = helpers.read_input()
    if "A" in lines[0]:
        s = bin(int(lines[0], 16))[2:]
    else:
        s = lines[0]
    packet = helpers.decode_packet(io.StringIO(s))
    packet.print()
    print(packet.eval())


main()
