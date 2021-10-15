from FenParser import FenParser

pawn_locs = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5, 5, 10, 25, 25, 10, 5, 5],
    [0, 0, 0, 20, 20, 0, 0, 0],
    [5, -5, -10, 0, 0, -10, -5, 5],
    [5, 10, 10, -20, -20, 10, 10, 5],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

knight_locs = [
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50]
]

bishop_locs = [
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [-10, 5, 5, 10, 10, 5, 5, -10],
    [-10, 0, 10, 10, 10, 10, 0, -10],
    [-10, 10, 10, 10, 10, 10, 10, -10],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20]
]

rook_locs = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 10, 10, 10, 10, 10, 10, 5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [0, 0, 0, 5, 5, 0, 0, 0]
]

queen_locs = [
    [-20, -10, -10, -5, -5, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 5, 5, 5, 0, -10],
    [-5, 0, 5, 5, 5, 5, 0, -5],
    [0, 0, 5, 5, 5, 5, 0, -5],
    [-10, 5, 5, 5, 5, 5, 0, -10],
    [-10, 0, 5, 0, 0, 0, 0, -10],
    [-20, -10, -10, -5, -5, -10, -10, -20]
]

king_locs = [
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-20, -30, -30, -40, -40, -30, -30, -20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [20, 20, 0, 0, 0, 0, 20, 20],
    [20, 30, 10, 0, 0, 10, 30, 20]
]

locs = {"P": pawn_locs, "N": knight_locs, "B": bishop_locs, "R": rook_locs, "Q": queen_locs}


class Evaluation:

    def __init__(self, board, color, eval_mode="s"):
        self.board = board
        self.board_fen = FenParser(board).parse()
        self.color = color
        self.eval_mode = eval_mode

    def basic_evaluation(self):
        col = 1 if self.color else 0
        if self.board.outcome():
            if self.board.outcome().winner is not None:
                return 10000 if self.board.outcome().winner == col else -10000
            elif self.board.outcome().winner is None:
                return 0
        if self.board.is_repetition():
            return 0
        if self.board.is_insufficient_material():
            return 0
        return None

    def simplified_evaluation(self):
        score = 0
        for piece, weight in [(1, 100), (2, 320), (3, 330), (4, 500), (5, 900), (6, 20000)]:
            score += weight * (
                    len(self.board.pieces(piece, self.color)) - len(self.board.pieces(piece, not self.color)))

        for row in range(1, len(self.board_fen) + 1):
            for col in range(1, len(self.board_fen[row - 1]) + 1):
                if self.board_fen[row - 1][col - 1] != " " and self.board_fen[row - 1][col - 1].lower() != "k":
                    piece = self.board_fen[row - 1][col - 1]
                    piece_weights = locs[piece.upper()]

                    if self.color:  # player plays white
                        score = score + piece_weights[row - 1][col - 1] if piece.isupper() \
                            else score - piece_weights[row - 1][col - 1]
                    else:  # player plays black
                        score = score + piece_weights[-row][col - 1] if not piece.isupper() \
                            else score - piece_weights[-row][col - 1]
        return score

    def eval(self, color=None):
        if color is not None:
            self.color = color
        b_eval = self.basic_evaluation()
        if b_eval is not None:
            return b_eval
        return self.simplified_evaluation()
