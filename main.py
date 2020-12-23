#! /usr/bin/env python3
# main.py
# programmed by Saito-Saito-Saito
# explained in https://Saito-Saito-Saito.github.io/reversi
# last update: 23/12/2020

from config import *
import IO
import board

# preset
logger = setLogger(__name__)

main_board = board.Board()
player = BLACK

main_board.BoardPrint()


while True:
    ### GAMESET JUDGE
    # NOTE: you must not control game_status here because out of the loop it must be GAME_PRC
    if main_board.gamesetjudge():
        break

    ### PLAYER OUTPUT
    if player == BLACK:
        print('○ TURN', end=' ')
    elif player == WHITE:
        print('● TURN', end=' ')
    else:
        logger.error('UNEXPECTED VALUE of PLAYER in the while loop')
        break

    ### PASS JUDGE
    if main_board.passjudge(player):
        print('BUT YOU CANNOT PUT ANYWHERE (PRESS ENTER TO PASS)')
        input()
        # player change
        player *= -1
        continue

    ### INPUT
    print('(X to give up) >>> ', end='')
    s = input()
    # give up
    if s in ['X', 'x']:
        main_board.winner = -player
        break
    else:
        square = IO.InputFormat(s)
        logger.info('motion = {}'.format(square))
    
    # invalid putting
    if square == False:
        print('INVALID INPUT')
        continue
    elif main_board.turn(player, *square) == FAILED:
        print('INVALID PUTTING')
        continue
    
    ### PLAYER CHANGE
    player *= -1

    main_board.BoardPrint()



print('\nGAME SET')

# in case of give up
if main_board.game_status == GAME_PRC:
    print('INTERRUPTION')
    if main_board.winner == BLACK:
        print('BLACK WINS')
    elif main_board.winner == WHITE:
        print('WHITE WINS')
    else:
        print('SYSTEM ERROR: DRAW')
# the other cases of game set
else:
    counter = main_board.countpiece()
    print('{} - {}'.format(counter[0], counter[1]))
    if counter[0] == counter[1]:
        print('DRAW')
    elif counter[0] > counter[1]:
        print('○ WINS')
    elif counter[0] < counter[1]:
        print('● WINS')
    else:
        logger.error('ILLOGICAL ATTITUDE out of the while loop')

print('\nGAME OVER\n')
