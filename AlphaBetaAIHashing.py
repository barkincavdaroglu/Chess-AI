from Evaluation import Evaluation


class AlphaBetaAIHashing():
    def __init__(self, depth, color, eval_mode="s"):
        self.maxDepth = depth
        self.color = color
        self.transposition = {}
        self.zobrist = None
        self.eval_mode = eval_mode

    def choose_move(self, board, zobrist, h, is_hashing):
        self.zobrist = zobrist
        val, move = self.AlphaBetaNegamax(board, self.maxDepth, -999999999, 999999999, h, self.color)
        return move, self.zobrist.hashUpdate(h, move, board, self.color)

    def terminalTest(self, board, depth):
        return depth == 0 or board.is_game_over()

    def evaluation(self, state, color):
        return Evaluation(state, self.color, self.eval_mode).eval(color)

    def AlphaBetaNegamax(self, board, depth, a, b, h, color, move=None):
        if move is not None:
            action_prior = board.pop()
            hash = self.zobrist.hashUpdate(h, move, board, color)
            board.push(action_prior)
        else:
            hash = h
        if hash in self.transposition and self.transposition[hash][1] >= depth:
            if self.transposition[hash][2] == "ex":
                return self.transposition[hash][0], move
            elif self.transposition[hash][2] == "lb":
                a = max(a, self.transposition[hash][0])
            elif self.transposition[hash][2] == "ub":
                b = min(b, self.transposition[hash][0])
            if a >= b:
                return self.transposition[hash][0], move

        if self.terminalTest(board, depth):
            score = self.evaluation(board, color)
            if score <= a:
                self.transposition[hash] = (score, depth, "lb")
            elif score >= b:
                self.transposition[hash] = (score, depth, "ub")
            else:
                self.transposition[hash] = (score, depth, "ex")
            return score, move

        moves = self.orderMoves(board, color)
        best, best_move = -999999999, move
        for _, action in moves:
            board.push(action)
            val = -self.AlphaBetaNegamax(board, depth - 1, -b, -a, hash, not color, action)[0]
            board.pop()
            if val > best:
                best, best_move = val, action
            if best > a:
                a = best
            if best >= b:
                break
        if best <= a:
            self.transposition[hash] = (best, depth, "lb")
        elif best >= b:
            self.transposition[hash] = (best, depth, "ub")
        else:
            self.transposition[hash] = (best, depth, "ex")
        return best, best_move

    def orderMoves(self, board, color):
        moveOrder = []
        for a in list(board.legal_moves):
            board.push(a)
            moveOrder.append((self.evaluation(board, color), a))
            board.pop()
        if color != self.color: # minimize it
            moveOrder.sort(key=lambda x: x[0])
        else:
            moveOrder.sort(key=lambda x: -x[0])
        return moveOrder
