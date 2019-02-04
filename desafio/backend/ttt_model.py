import random
import numpy as np
from datetime import datetime
 
WINSUMS = [3, 6]
BSIZE = 3
WIN = "win"
LOSE = "lose"


class TTTBoard:
    def __init__(self):
        self.board = np.zeros((BSIZE,BSIZE), dtype=np.int8)
        self.starttime = datetime.now()

    def mark(self, row, col, player):
        try:
            if (self.board[row][col] == 0):
                self.board[row][col] = player
            else:
                return False
        except(IndexError):
            return False

        return True

    def checkwin(self):
        for i in range(BSIZE):
            rowsum = self.board[i].sum()
            colsum = self.board[:,i].sum()

            if (0 not in self.board[i] and rowsum in WINSUMS):
                return rowsum / BSIZE
            if (0 not in self.board[:,i] and colsum in WINSUMS):
                return colsum / BSIZE

        diagonals = [
                self.board.diagonal(),
                self.board[list(reversed(range(BSIZE)))].diagonal()
        ]

        for diagonal in diagonals:
            if (0 not in diagonal and diagonal.sum() in WINSUMS):
                return diagonal.sum() / BSIZE
        
        return 0

    def checkdraw(self):
        return 0 == np.count_nonzero(self.board == 0)


class TTTPlayer:
    def __init__(self):
        self.moves = dict()
        self.curgame = []
        self.pnumber = -1

    def start_game(self, pnumber):
        self.pnumber = pnumber
        self.curgame = []

    def make_move(self, board):
        board_state = tuple(map(tuple, board))
        print(board_state)
        
        if (len(self.curgame) == 0):
            if (board[BSIZE // 2][BSIZE // 2] == 0):
                next_move = (BSIZE // 2, BSIZE // 2)
            else:
                next_move = random.choice([(0, 0), (0, BSIZE - 1), (BSIZE - 1, 0), (BSIZE - 1, BSIZE - 1)])
        else:
            possib_moves = []
            move_weights = []
            dejavu = board_state in self.moves 
            
            for row in range(BSIZE):
                for col in range(BSIZE):
                    pos = (row, col)
                    if (board[row][col] == 0):
                        if (dejavu and pos in self.moves[board_state]):
                            possib_moves.append(pos)
                            move_weights.append((1 + self.moves[board_state][pos][WIN]) / (1 + self.moves[board_state][pos][LOSE]))
                        else:
                            possib_moves.append(pos)
                            move_weights.append(1.0)

            next_move = random.choices(possib_moves, weights=move_weights)[0]

        self.curgame.append((board_state, next_move))

        return next_move

    def learn(self, result):
        for board_state, move in self.curgame:
            if (board_state not in self.moves):
                self.moves[board_state] = dict()
            if (move not in self.moves[board_state]):
                self.moves[board_state][move] = {WIN: 0, LOSE: 0}

            self.moves[board_state][move][result] += 1



