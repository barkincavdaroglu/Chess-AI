import chess
import chess.polyglot
from Zobrist import ZobristHash
import time


class ChessGame:
    def __init__(self, player1, player2, is_hash):
        board = chess.Board()
        zobrist = ZobristHash()
        self.zobrist = zobrist
        self.board = board
        self.players = [player1, player2]
        self.h = zobrist.zobristHash(board)
        self.is_hashing = is_hash
        self.times = []

    def make_move(self):
        player = self.players[1 - int(self.board.turn)]
        start = time.time()
        if self.is_hashing:
            move, updated_hash = player.choose_move(self.board, self.zobrist, self.h, True)
            self.h = updated_hash
        else:
            move = player.choose_move(self.board, self.zobrist, self.h, False)
        end = time.time()
        self.times.append(end - start)
        self.board.push(move)  # Make the move

    def is_game_over(self):
        return self.board.is_game_over()

    def __str__(self):
        column_labels = "\n----------------\na b c d e f g h\n"
        board_str = str(self.board) + column_labels

        # did you know python had a ternary conditional operator?
        move_str = "White to move" if self.board.turn else "Black to move"

        return board_str + "\n" + move_str + "\n"
