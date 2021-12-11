#!/usr/bin/python3

import random

for i in range(10):
    print(*list(random.randrange(1, 10) for i in range(10)), sep='')
