#! /usr/bin/env python3
# check.py

import copy

from config import *


class Board:
    def __init__(self, input_board=[]):
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
            self.game_status = GAME_PRC
            self.winner = EMPTY
            

    def BoardPrint(self):
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
                    logging.critical('UNEXPECTED PLAYER VALUE in BoardPrint')
                    return False
            print(' {}'.format(row + 1))
            print('\t   -------------------------------')
        print('\t    a   b   c   d   e   f   g   h')
        print('\n')

    
    def putjudge(self, player, row, col, direction):
        # out of the board
        if not (InBoard(row) and InBoard(col)):
            logging.debug('{}, {}\tOUT OF THE BOARD'.format(row, col))
            return False

        piece = self.board[row][col]
        
        # EMPTY
        if piece == EMPTY:
            logging.debug('{}, {}\tREACHED TO EMPTY'.format(row, col))
            return False
        # OWN
        elif piece == player:
            logging.debug('{}, {}\tREACHED TO OWN PIEE'.format(row, col))
            return True
        # OPPONENT'S
        elif piece == -player:
            return self.putjudge(player, row + direction[ROW], col + direction[COL], direction)
        # ERROR
        else:
            logging.error('UNEXPECTED VALUE of PLAYER in putjudge')
            return False
        
    
    def turn(self, player, row, col):
        # out of the board
        if not (InBoard(row) and InBoard(col)):
            logging.info('OUT OF THE BOARD')
            return False

        # there is already a piece
        if self.board[row][col] != EMPTY:
            logging.info('THERE IS ALREADY A PIECE')
            return False

        turned = False
        # searching all the direction for available one
        for direction in WHOLE_DIRECTION:
            focused = [row + direction[ROW], col + direction[COL]]
            if not (InBoard(focused[ROW]) and InBoard(focused[COL])):
                continue
            next_piece = self.board[focused[ROW]][focused[COL]]
            logging.debug('direc = {}, next_piece = {}'.format(direction, next_piece))
            # in case available
            if next_piece == -player and self.putjudge(player, focused[ROW], focused[COL], direction):
                while self.board[focused[ROW]][focused[COL]] == -player:
                    self.board[focused[ROW]][focused[COL]] = player
                    focused[ROW] += direction[ROW]
                    focused[COL] += direction[COL]
                    turned = True
                
        # in case a piece was turned
        if turned:
            self.board[row][col] = player
            return True
        else:
            logging.info('THERE IS NO DIRECTION AVAILABLE')
            return False

    
    def passjudge(self, player):
        # searching all EMPTY that can turn
        for row in range(SIZE):
            for col in range(SIZE):
                if self.board[row][col] == EMPTY:
                    for direction in WHOLE_DIRECTION:
                        focused = [row + direction[ROW], col + direction[COL]]
                        if not (InBoard(focused[ROW]) and InBoard(focused[COL])):
                            continue
                        if self.board[focused[ROW]][focused[COL]] == -player and self.putjudge(player, focused[ROW], focused[COL], direction):
                            logging.info('THERE IS {}, {}'.format(row, col))
                            return False
        
        # completing all the loop, there is no square that you can put
        return True


    def countpiece(self):
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
        

    def gamesetjudge(self):
        # if either can put, it's not gameset
        if self.passjudge(BLACK) == False or self.passjudge(WHITE) == False:
            logging.debug('either can put yet')
            return False
        else:
            self.game_status = GAME_SET
            return True
