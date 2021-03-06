from typing import Dict

import helpers

import itertools
import collections

valid_numbers = dict(abcefg='0', cf='1', acdeg='2', acdfg='3', bcdf='4', abdfg='5', abdefg='6', acf='7', abcdefg='8', abcdfg='9')
segments = 'abcdefg'

def xform(s: str, m: Dict[int, str]) -> str:
    return ''.join(sorted(s.translate(m)))

def main() -> None:
    lines = [ l.split(' | ') for l in helpers.read_input()]
    mappings = [ str.maketrans(dict(zip(permutation, segments))) for permutation in itertools.permutations(segments) ]
    for left, right in lines:
        entries = [ ''.join(sorted(w)) for w in left.split(' ') + right.split(' ')]
        for mapping in mappings:
            xformed_valid_numbers = { xform(k, mapping): v for k, v in valid_numbers.items() }
            if all(entry in xformed_valid_numbers for entry in entries):
                new_left = ''.join([xformed_valid_numbers[''.join(sorted(v))] for v in left.split()])
                new_right = ''.join([xformed_valid_numbers[''.join(sorted(v))] for v in right.split()])
                print(f'yay {new_left} | {new_right}')
                break

main()
