# Chess-AI
Use chess_t.py as your entry point.
There are 3 AI players: AlphaBetaAI.py, AlphaBetaAIHashing.py, and MinimaxAI.py. 
AlphaBetaAI and MinimaxAI are self-explanatory. AlphaBetaAIHashing uses Negamax with
zobrist hash and transposition tables to speed up the process. 
Pass in True / False
for each AI player, representing its color in the game (True for white, False for black).
There are 4 parameters to pass into AlphaBetaAI and MinimaxAI: depth, color, 
is_iterative=False, and eval_mode=“s”. Depth and color are self-explanatory. 
is_iterative should be True if you want to use IDS, and False otherwise (default value). 
