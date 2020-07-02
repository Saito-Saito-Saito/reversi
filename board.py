#! /usr/bin/env python3
# board.py
# programmed by Saito-Saito-Saito
# explained in https://Saito-Saito-Saito.github.io/reversi
# last update: 2/7/2020

import copy

from config import *

local_logger = setLogger(__name__)


class Board:
    def __init__(self, input_board=[], *, status=GAME_PRC, winner=EMPTY, logger=None):
        if len(input_board) == SIZE:
            self.board = copy.deepcopy(input_board)
        else:
            self.board = []
            for row in range(SIZE):
                self.board.append([0 for col in range(SIZE)])
            self.board[int(SIZE / 2) - 1][int(SIZE / 2) - 1] = WHITE
            self.board[int(SIZE / 2) - 1][int(SIZE / 2)] = BLACK
            self.board[int(SIZE / 2)][int(SIZE / 2) - 1] = BLACK
            self.board[int(SIZE / 2)][int(SIZE / 2)] = WHITE
            # 0:進行中(途中)PRC　1:決着SET
        self.game_status = status
        self.winner = winner
        self.logger = logger or local_logger
            

    def BoardPrint(self, logger=None):
        logger = logger or self.logger
        
        print('\n')
        print('\t    a   b   c   d   e   f   g   h')
        print('\t   -------------------------------')
        for row in range(SIZE):
            print('\t{} |'.format(row + 1), end='')
            for col in range(SIZE):
                if self.board[row][col] == EMPTY:
                    print('   |', end='')
                elif self.board[row][col] == WHITE:
                    print(' ● |', end='')
                elif self.board[row][col] == BLACK:
                    print(' ○ |', end='')
                else:
                    logger.critical('UNEXPECTED PLAYER VALUE in BoardPrint')
                    return False
            print(' {}'.format(row + 1))
            print('\t   -------------------------------')
        print('\t    a   b   c   d   e   f   g   h')
        print('\n')

    
    """
        turnjudge judges whether the piece can be turned
        if player put a piece on [R, C] ...
        1.  check whether [R+direc[ROW], C+direc[COL]]==-player
        2.  if yes and turnjudge(player, R+direc..., C+direc..., direc)==True, you can turn the direction when you put a piece on [R,C]
        3.  if yes but turnjudge(player, R+direc..., C+direc..., direc)==False, you cannot turn the direction when you put a piece on [R, C] (it does not always mean that you cannot put a piece there)
    """
    def turnjudge(self, player, row, col, direction: list, logger=None):
        logger = logger or self.logger
        
        # out of the board
        if not (InBoard(row) and InBoard(col)):
            logger.debug('{}, {}\tOUT OF THE BOARD'.format(row, col))
            return False

        # BLACK, WHITE or EMPTY
        piece = self.board[row][col]
        
        # EMPTY
        if piece == EMPTY:
            logger.debug('{}, {}\tREACHED TO EMPTY'.format(row, col))
            return False
        # OWN
        elif piece == player:
            logger.debug('{}, {}\tREACHED TO OWN PIEE'.format(row, col))
            return True
        # OPPONENT'S
        elif piece == -player:
            return self.turnjudge(player, row + direction[ROW], col + direction[COL], direction)
        # ERROR
        else:
            logger.error('UNEXPECTED VALUE of PLAYER in putjudge')
            return False
        
    
    def turn(self, player, row, col, logger=None):
        logger = logger or local_logger
        
        # out of the board
        if not (InBoard(row) and InBoard(col)):
            logger.info('OUT OF THE BOARD')
            return False

        # there is already a piece
        if self.board[row][col] != EMPTY:
            logger.info('THERE IS ALREADY A PIECE')
            return False

        turned = False
        # searching all the direction for available one
        for direction in WHOLE_DIRECTION:
            focused = [row + direction[ROW], col + direction[COL]]
            if not (InBoard(focused[ROW]) and InBoard(focused[COL])):
                continue
            next_piece = self.board[focused[ROW]][focused[COL]]
            logger.debug('direc = {}, next_piece = {}'.format(direction, next_piece))
            # in case available
            if next_piece == -player and self.turnjudge(player, focused[ROW], focused[COL], direction):
                while self.board[focused[ROW]][focused[COL]] == -player:
                    self.board[focused[ROW]][focused[COL]] = player
                    focused[ROW] += direction[ROW]
                    focused[COL] += direction[COL]
                    turned = True
                
        # in case a piece was turned
        if turned:
            self.board[row][col] = player
            return True
        # in case any piece was not turned
        else:
            logger.info('THERE IS NO DIRECTION AVAILABLE')
            return False

    
    def passjudge(self, player, logger=None):
        logger = logger or self.logger
        
        # searching all EMPTY squares that can turn
        for row in range(SIZE):
            for col in range(SIZE):
                if self.board[row][col] == EMPTY:
                    for direction in WHOLE_DIRECTION:
                        focused = [row + direction[ROW], col + direction[COL]]
                        if not (InBoard(focused[ROW]) and InBoard(focused[COL])):
                            continue
                        if self.board[focused[ROW]][focused[COL]] == -player and self.turnjudge(player, focused[ROW], focused[COL], direction):
                            logger.info('THERE IS {}, {}'.format(row, col))
                            return False
        
        # completing all the loop, there is no square that you can put a piece
        return True


    def countpiece(self, logger=None):
        logger = logger or self.logger
        
        # count up all pieces
        self.b_count = 0
        self.w_count = 0
        for row in range(SIZE):
            for col in range(SIZE):
                if self.board[row][col] == BLACK:
                    self.b_count += 1
                elif self.board[row][col] == WHITE:
                    self.w_count += 1
        return [self.b_count, self.w_count]
        

    def gamesetjudge(self, logger=None):
        logger = logger or self.logger
        
        # if either can put, it's not gameset
        if self.passjudge(BLACK) == False or self.passjudge(WHITE) == False:
            logger.debug('either can put yet')
            return False
        else:
            self.game_status = GAME_SET
            return True
