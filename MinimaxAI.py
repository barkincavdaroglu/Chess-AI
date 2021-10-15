from Evaluation import Evaluation


class MinimaxAI():
    def __init__(self, depth, color, is_iterative=False, eval_mode="s"):
        self.maxDepth = depth
        self.color = color
        self.is_iterative = is_iterative
        self.eval_mode = eval_mode
        self.num_of_calls = 0

    def choose_move(self, board, *argv):
        if self.is_iterative:
            return self.MinimaxDecisionIterative(board)
        else:
            return self.MinimaxDecisionNonIterative(board)[0]

    def terminalTest(self, board, depth):
        return depth >= self.maxDepth or board.is_game_over()

    # This is the stupid "evaluation" function for
    # Task 1 where we try to search if a move will
    # lead to a checkmate or not.
    def utility(self, state):
        if state.outcome() and state.outcome().winner:
            return 1 if state.outcome().winner == 1 else -1
        else:
            return 0

    def evaluation(self, state):
        return Evaluation(state, self.color, self.eval_mode).eval()

    def MinimaxDecisionNonIterative(self, board):
        maxVal, bestMove = self.MaxValue(board, 0)
        print("Minimax Value is: " + str(maxVal))
        print("Number of calls made to Minimax at depth " + str(self.maxDepth) + " is " + str(self.num_of_calls))
        return bestMove, maxVal

    # Since basic Minimax is not pruning the search tree,
    # I am not sure how useful IDS will be. But I have
    # implemented it just in case.
    def MinimaxDecisionIterative(self, board):
        best_move, best_score = None, float('-inf')
        maxDepth = self.maxDepth
        for d in range(1, maxDepth + 1):
            self.maxDepth = d
            argmax, maxVal = self.MinimaxDecisionNonIterative(board)
            if maxVal > best_score:
                best_move, best_score = argmax, maxVal
        self.maxDepth = maxDepth
        return best_move

    def MaxValue(self, state, depth):
        if self.terminalTest(state, depth):
            return self.evaluation(state), None
        v, best_move = float('-inf'), None
        for action in list(state.legal_moves):
            state.push(action)
            minVal = self.MinValue(state, depth + 1)
            if minVal >= v:
                best_move, v = action, minVal
            self.num_of_calls += 1
            state.pop()
        return v, best_move

    def MinValue(self, state, depth):
        if self.terminalTest(state, depth):
            return self.evaluation(state)
        v = float('inf')
        for action in list(state.legal_moves):
            state.push(action)
            v = min(v, self.MaxValue(state, depth + 1)[0])
            self.num_of_calls += 1
            state.pop()
        return v
