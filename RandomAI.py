#import chess
import random
from time import sleep

class RandomAI():
    def __init__(self, color):
        self.color = color

    def choose_move(self, board, zobrist, h, is_hashing):
        moves = list(board.legal_moves)
        move = random.choice(moves)
        sleep(1)   # I'm thinking so hard.
        print("Random AI recommending move " + str(move))
        if is_hashing:
            updated_h = zobrist.hashUpdate(h, move, board, self.color)
            return move, updated_h
        else:
            return move
