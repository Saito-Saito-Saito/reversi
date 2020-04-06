#! /usr/bin/env python3
# __main__.py


import sys
import logging

logging.basicConfig(level=logging.WARNING, format='%(levelname)s - %(filename)s - L%(lineno)d - %(message)s')


# board is 8 * 8
SIZE = 8
if int(SIZE / 2) != SIZE / 2:
    logging.error('SIZE VALUE HAS TO BE EVEN')
    sys.exit()


# rows & columns
ROW = 0
COL = 1

EMPTY = 0
B = BLACK = 1
W = WHITE = -1


WHOLE_DIRECTION = [
    [-1, -1], [-1, 0], [-1, 1],
    [0, -1], [0, 1],
    [1, -1], [1, 0], [1, 1]
]


def InBoard(subject):
    if 0 <= subject < SIZE:
        return True
    else:
        return False