#! /usr/bin/env python3
# IO.py
# programmed by Saito-Saito-Saito
# last update: 4/5/2020


import config


# translate user's input into the index of the square
def InputFormat(s):
    if len(s) != 2:
        config.logging.info('len(s) == {}'.format(len(s)))
        return False
    elif s[0].isdecimal() and config.InBoard(int(s[0]) - 1) and ord('a') <= ord(s[1]) <= ord('h'):
        return [int(s[0]) - 1, ord(s[1]) - ord('a')]
    elif s[1].isdecimal() and config.InBoard(int(s[1]) - 1) and ord('a') <= ord(s[0]) <= ord('h'):
        return [int(s[1]) - 1, ord(s[0]) - ord('a')]
    else:
        config.logging.info('OUT OF FORMAT')
        return False
