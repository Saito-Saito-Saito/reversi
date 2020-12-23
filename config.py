#! /usr/bin/env python3
# config.py
# programmed by Saito-Saito-Saito
# explained in https://Saito-Saito-Saito.github.io/reversi
# last update: 23/12/2020


import sys
from logging import getLogger, StreamHandler, FileHandler, Formatter, DEBUG, INFO, WARNING, ERROR, CRITICAL


### LOG SETTINGS
DEFAULT_LOG_ADDRESS = 'log.txt'
DEFAULT_LOG_FORMAT = Formatter('%(asctime)s - %(levelname)s - logger:%(name)s - %(filename)s - L%(lineno)d - %(funcName)s - %(message)s')

# set up function
def setLogger(name='default', level=DEBUG, *, fhandler=None, fhandler_level=DEBUG, filename=DEFAULT_LOG_ADDRESS, filemode='w', fileformat=DEFAULT_LOG_FORMAT, shandler=None, shandler_level=CRITICAL, streamformat=DEFAULT_LOG_FORMAT):
    logger = getLogger(name)
    logger.setLevel(level)
    
    # file handler
    fhandler = fhandler or FileHandler(filename, mode=filemode)
    fhandler.setLevel(fhandler_level)
    fhandler.setFormatter(fileformat)
    logger.addHandler(fhandler)
    
    # stream handler
    shandler = shandler or StreamHandler()
    shandler.setLevel(shandler_level)
    shandler.setFormatter(streamformat)
    logger.addHandler(shandler)
    
    return logger


logger = setLogger(__name__)


# board is 8 * 8
SIZE = 8
if int(SIZE / 2) != SIZE / 2:
    logger.error('SIZE VALUE HAS TO BE EVEN')
    print('SYSTEM ERROR')
    sys.exit()


# rows & columns index
ROW = 0
COL = 1


# piece values
EMPTY = 0
B = BLACK = 1
W = WHITE = -1


# game proceeding/set
GAME_PRC = 0
GAME_SET = 1


# for return
SUCCEEDED = True
FAILED = False


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