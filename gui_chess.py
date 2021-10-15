# brew install pyqt
from PyQt5 import QtGui, QtSvg
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.QtWidgets import QApplication, QWidget
import sys
import chess, chess.svg
from RandomAI import RandomAI
from MinimaxAI import MinimaxAI
from ChessGame import ChessGame
from AlphaBetaAI import AlphaBetaAI
from AlphaBetaAIHashing import AlphaBetaAIHashing

import random
import sys
sys.setrecursionlimit(1500)


class ChessGui:
    def __init__(self, player1, player2, is_hashing):
        self.player1 = player1
        self.player2 = player2

        self.game = ChessGame(player1, player2, is_hashing)

        self.app = QApplication(sys.argv)
        self.svgWidget = QtSvg.QSvgWidget()
        self.svgWidget.setGeometry(50, 50, 400, 400)
        self.svgWidget.show()


    def start(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.make_move)
        self.timer.start(10)

        self.display_board()

    def display_board(self):
        svgboard = chess.svg.board(self.game.board)

        svgbytes = QByteArray()
        svgbytes.append(svgboard)
        self.svgWidget.load(svgbytes)

    def make_move(self):
        self.display_board()
        if not self.game.is_game_over():
            print("making move, white turn " + str(self.game.board.turn))
            self.game.make_move()
        else:
            aba = self.game.board.outcome()
            print("Average time AlphaBetaAI took for each move is " + str(sum(self.game.times) / len(self.game.times)))
            print(aba)
            return




if __name__ == "__main__":

    random.seed(1)

    #player_ronda = RandomAI()

    # to do: gui does not work well with HumanPlayer, due to input() use on stdin conflict
    # with event loop.

    player1 = RandomAI(True)#AlphaBetaAI(3, True)#MinimaxAI(3, True)
    player2 = AlphaBetaAI(3, False, True)#AlphaBetaAIHashing(3, False, "s")#MinimaxAI(3, False, False)#AlphaBetaAI(3, False, True, "s") #AlphaBetaAI(5, False, True)#MinimaxAI(3, False, True) #RandomAI()#AlphaBetaAI(3, False)

    game = ChessGame(player1, player2, False)
    gui = ChessGui(player1, player2, False)

    gui.start()

    sys.exit(gui.app.exec_())
