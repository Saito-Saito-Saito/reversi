#! /usr/bin/env python3
# __main__.py

from config import *
import IO
import board

main_board = board.Board()
player = BLACK
turn = 1

main_board.BoardPrint()


while True:
    ### GAMESET JUDGE
    if main_board.gamesetjudge():
        break

    ### PLAYER OUTPUT
    if player == BLACK:
        print('○ TURN', end=' ')
    elif player == WHITE:
        print('● TURN', end=' ')
    else:
        logging.error('UNEXPECTED VALUE of PLAYER in the while loop')
        winner = EMPTY
        break

    ### PASS CHECK
    if main_board.passjudge(player):
        print('BUT YOU CANNOT PUT ANYWHERE (PRESS ENTER TO PASS)')
        input()
        player *= -1
        continue

    ### INPUT
    print('(X to give up) >>> ', end='')
    s = input()
    if s in ['X', 'x']:
        winner = -player
        break
    else:
        motion = IO.InputFormat(s)
        logging.info('motion = {}'.format(motion))
    
    if motion == False:
        print('INVALID INPUT')
        continue
    elif main_board.turn(player, motion[0], motion[1]) == False:
        print('INVALID PUT')
        continue
    
    # PLAYER CHANGE
    player *= -1

    main_board.BoardPrint()



print('\nGAME SET')
counter = main_board.countpiece()

try:
    if winner == EMPTY:
        print('SYSTEM ERROR: DRAW')
    elif winner == BLACK:
        print('BLACK WINS')
    elif winner == WHITE:
        print('WHITE WINS')
except:
    counter = main_board.countpiece()
    print('{} - {}'.format(counter[0], counter[1]))
    if counter[0] == counter[1]:
        print('DRAW')
    elif counter[0] > counter[1]:
        print('BLACK WINS')
    elif counter[0] < counter[1]:
        print('WHITE WINS')
    else:
        logging.error('ILLOGICAL ATTITUDE out of the while loop')

print('\nGAME OVER\n')
