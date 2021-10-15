from Evaluation import Evaluation
from MinimaxAI import MinimaxAI


class AlphaBetaAI():
    def __init__(self, depth, color, is_iterative=False, eval_mode="s"):
        self.maxDepth = depth
        self.color = color
        self.iterative = is_iterative
        self.transposition = {}
        self.eval_mode = eval_mode
        self.num_of_calls = 0
        self.minimax = MinimaxAI(depth, color)

    def choose_move(self, board, *args):
        if self.iterative:
            move, score = self.AlphaBetaSearchIterativeWithoutPrior(board, self.maxDepth)
            #print("Number of calls made to AlphaBeta with maxDepth of " + str(self.maxDepth) + " is " + str(self.num_of_calls))
            #minmax_move, minmax_score = self.minimax.choose_move(board)
            #print(score, minmax_score)
            return move
        else:
            move, score = self.AlphaBetaSearch(board)
            # Uncomment the code below to verify Minimax and AlphaBeta are
            # returning the same values.
            # minmax_move, minmax_score = self.minimax.choose_move(board)
            # print(score,minmax_score)
            print("Number of calls made to AlphaBeta with maxDepth of " + str(self.maxDepth) + " is " + str(self.num_of_calls))
            return move

    def terminalTest(self, board, depth):
        return depth >= self.maxDepth or board.is_game_over()

    def utility(self, state):
        if state.outcome() and state.outcome().winner:
            return 1 if state.outcome().winner == 0 else -1
        else:
            return 0

    def evaluation(self, state):
        return Evaluation(state, self.color, self.eval_mode).eval()

    def orderMoves(self, board, color):
        moveOrder = []
        for a in list(board.legal_moves):
            board.push(a)
            moveOrder.append((self.evaluation(board), a))
            board.pop()
        if color != self.color: # minimize it
            moveOrder.sort(key=lambda x: x[0])
        else:
            moveOrder.sort(key=lambda x: -x[0])
        return moveOrder

    def AlphaBetaSearchIterativeWithoutPrior(self, board, maxDepth):
        best_score, best_move = 0, None

        for d in range(1, maxDepth + 1):
            self.maxDepth = d
            best_move, best_score = self.AlphaBetaSearch(board)
            print(best_score, best_move)

        self.maxDepth = maxDepth
        return best_move, best_score

    def AlphaBetaSearchIterativeWithPrior(self, board, maxDepth):
        moveOrder, replace = self.orderMoves(board, self.color), []
        best_score, best_move = moveOrder[0]

        for d in range(1, maxDepth + 1):
            self.maxDepth = d
            maxVal, argmax = float('-inf'), None
            for cost_of_a, a in moveOrder:
                board.push(a)
                minVal = self.MinValue(board, float('-inf'), float('inf'), 1)
                self.num_of_calls += 1
                if minVal >= maxVal:
                    argmax, maxVal = a, minVal
                board.pop()
                replace.append((minVal, a))
            moveOrder = sorted(replace, key=lambda x: -x[0])
            best_move, best_score = argmax, maxVal
        self.maxDepth = maxDepth
        return best_move, best_score

    def AlphaBetaSearch(self, board):
        maxVal, bestMove = self.MaxValue(board, float('-inf'), float('inf'), 0)
        return bestMove, maxVal

    def MaxValue(self, state, a, b, depth):
        if self.terminalTest(state, depth):
            return self.evaluation(state), None
        v, best_move = float('-inf'), None
        moveOrder = self.orderMoves(state, self.color)
        for _, action in moveOrder:
            state.push(action)
            minVal = self.MinValue(state, a, b, depth + 1)
            self.num_of_calls += 1
            if minVal > v:
                v, best_move = minVal, action
            if v >= b:
                state.pop()
                return v, best_move
            a = max(a, v)
            state.pop()
        return v, best_move

    def MinValue(self, state, a, b, depth):
        if self.terminalTest(state, depth):
            return self.evaluation(state)
        v = float('inf')
        moveOrder = self.orderMoves(state, not self.color)
        for _, action in moveOrder:
            state.push(action)
            v = min(v, self.MaxValue(state, a, b, depth + 1)[0])
            self.num_of_calls += 1
            if v <= a:
                state.pop()
                return v
            b = min(b, v)
            state.pop()
        return v
