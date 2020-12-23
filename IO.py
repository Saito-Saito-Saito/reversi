#! /usr/bin/env python3
# IO.py
# programmed by Saito-Saito-Saito
# explained in https://Saito-Saito-Saito.github.io/reversi
# last update: 23/12/2020


import config
local_logger = config.setLogger(__name__)



# translate user's input into the index of the square
def InputFormat(s):
    if len(s) != 2:
        local_logger.info('len(s) == {}'.format(len(s)))
        return config.FAILED
    elif s[0].isdecimal() and config.InBoard(int(s[0]) - 1) and ord('a') <= ord(s[1]) <= ord('h'):
        return [int(s[0]) - 1, ord(s[1]) - ord('a')]
    elif s[1].isdecimal() and config.InBoard(int(s[1]) - 1) and ord('a') <= ord(s[0]) <= ord('h'):
        return [int(s[1]) - 1, ord(s[0]) - ord('a')]
    else:
        local_logger.info('OUT OF FORMAT')
        return config.FAILED
