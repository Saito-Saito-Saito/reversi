#! /usr/bin/env python3
# config.py
# programmed by Saito-Saito-Saito
# last update: 4/5/2020


import sys
import logging

logging.basicConfig(level=logging.WARNING, format='%(levelname)s - %(filename)s - L%(lineno)d - %(message)s')


# board is 8 * 8
SIZE = 8
if int(SIZE / 2) != SIZE / 2:
    logging.error('SIZE VALUE HAS TO BE EVEN')
    sys.exit()


# rows & columns index
ROW = 0
COL = 1

EMPTY = 0
B = BLACK = 1
W = WHITE = -1


# game processing/set
GAME_PRC = 0
GAME_SET = 1


# direction is represented as follows: [toROW - frROW, toCOL - frCOL]
WHOLE_DIRECTION = [
    [-1, -1], [-1, 0], [-1, 1],
    [0, -1], [0, 1],
    [1, -1], [1, 0], [1, 1]
]


# whether the index is in the board
def InBoard(subject):
    if 0 <= subject < SIZE:
        return True
    else:
        return False