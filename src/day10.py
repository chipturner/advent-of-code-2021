import helpers

import itertools
import collections

chunks = {"(": ")", "[": "]", "{": "}", "<": ">"}
scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
close_scores = dict(zip(")]}>", range(1, 5)))


def main() -> None:
    lines = helpers.read_input()

    valid = []
    score = 0
    score2s = []
    for line in lines:
        bad = False
        stack = []
        for ch in line:
            if ch in chunks:
                stack.append(ch)
            else:
                if chunks[stack[-1]] != ch:
                    score += scores[ch]
                    bad = True
                    break
                else:
                    stack.pop(-1)
        if not bad:
            valid.append(line)
            score = 0
            for ch in reversed(stack):
                score *= 5
                score += close_scores[chunks[ch]]
            score2s.append(score)
    print(sorted(score2s)[len(score2s) // 2])


main()
