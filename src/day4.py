import helpers
import numpy

import itertools
import collections
from typing import List

def card_wins(card):
    d = numpy.array(card)
    dt = d.transpose()
    for row in d:
        if numpy.sum(row) == 0:
            return True
    for row in dt:
        if numpy.sum(row) == 0:
            return True
    return False


def main() -> None:
    lines = helpers.read_input()
    numbers = [int(v) for v in lines[0].split(",")]

    cards = []
    cur_card: List[List[int]] = []
    for line in lines[2:]:
        if not line:
            cards.append(cur_card)
            cur_card = []
        else:
            cur_card.append(list(int(x) for x in line.split()))
    cards.append(cur_card)

    print(cards)
    winners = {}
    for num in numbers:
        for idx in range(len(cards)):
            if idx in winners:
                continue
            card = cards[idx]
            for i in range(len(card)):
                for j in range(len(card[0])):
                    if card[i][j] == num:
                        card[i][j] = 0
            if card_wins(card):
                print(num)
                s = sum(sum(r) for r in card)
                print(s)
                print(card)
                print(num * s)
                winners[idx] = 1


main()
