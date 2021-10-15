import random
from FenParser import FenParser
import chess

pieces = {
    "R": 4,
    "N": 3,
    "B": 2,
    "Q": 5,
    "K": 6,
    "P": 1,
    "r": 10,
    "n": 9,
    "b": 8,
    "q": 11,
    "k": 12,
    "p": 7,
}

num_to_pieces = {
    1: "P",
    2: "B",
    3: "N",
    4: "R",
    5: "Q",
    6: "K",
    7: "p",
    8: "b",
    9: "n",
    10: "r",
    11: "q",
    12: "k"
}


# https://en.wikipedia.org/wiki/Zobrist_hashing
class ZobristHash:
    def __init__(self):
        self.table = [0] * (64 * 12 + 13)
        for i in range(64 * 12 + 13):
            self.table[i] = random.getrandbits(64)

    def zobristHash(self, board):
        parser = FenParser(board)
        board_parsed = parser.parse()

        h = 0
        for i in range(8):
            for k in range(8):
                if board_parsed[i][k] != " ":
                    j = pieces[board_parsed[i][k]]
                    h ^= self.table[i * k + k + (j - 1)]
        return h

    def hashUpdate(self, hash, move, board, player):
        h = hash
        from_sq, to_sq, = move.from_square, move.to_square
        piece_type_rmvl = num_to_pieces[board.piece_type_at(from_sq)]
        h ^= self.table[(from_sq % 8) * 8 + pieces[piece_type_rmvl]]
        h ^= self.table[(to_sq % 8) * 8 + pieces[piece_type_rmvl]]

        if board.piece_type_at(to_sq) is not None:
            captured_piece = (board.piece_type_at(to_sq))
            captured_piece = num_to_pieces[captured_piece]
            h ^= self.table[(to_sq % 8) * 8 + pieces[captured_piece]]

        if board.is_castling(move):
            if board.is_kingside_castling(move):
                if player: # white player, kingside / short castling
                    h ^= self.table[768]
                else: # black player, kingside / short castling
                    h ^= self.table[770]
            elif board.is_queenside_castling(move):
                if player: # white player, queenside / long castling
                    h ^= self.table[769]
                else: # black player, queenside / long castling
                    h ^= self.table[771]

        if board.is_en_passant(move):
            h ^= self.table[768 + chess.square_file(to_sq)]

        if not player:
            h ^= self.table[780]

        return h
