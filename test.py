import sys
from gui import *
import game
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal
import time


class WaitForMove(QThread):
    done = pyqtSignal(int, int)
    error = pyqtSignal(Exception)

    def __init__(self, player, board):
        super(WaitForMove, self).__init__()
        self.player = player
        self.board = board

    def run(self):
        print('Waiting for move')
        try:
            move = self.player.choose_move(self.board)
        except game.boards.GameEndedError as e:
            print('error ', e)
            self.error.emit(e)
            return
        print('Move')
        self.done.emit(*move)


class QSinglePlayerGame(QWidget):
    def __init__(self, playerIsNotFirst=False):
        super(QSinglePlayerGame, self).__init__()
        # self.bot = game.players.ai.RandomBot('Bot')
        self.bot = game.players.ai.EuristicsBot('Bot')
        self.board = game.boards.Macroboard()
        layout = QVBoxLayout()
        layout.addWidget(QMacroBoard(self.buttonClick))
        # tmp
        layout.addWidget(QPushButton('&Test'))
        self.setLayout(layout)
        if playerIsNotFirst:
            self.qBoard.setClickEnabled(False)
            self.botMove()

    @property
    def qBoard(self):
        return self.layout().itemAt(0).widget()

    def makeBotMove(self, px, py):
        try:
            self.board.make_move(px, py)
        except game.boards.IllegalMoveError as err:
            print(err)
        except game.boards.GameEndedError as err:
            print(err)
        self.qBoard.updateBoard(self.board)
        self.qBoard.setClickEnabled(True)

    def botMoveError(self, e):
        print(e)

    def botMove(self):
        self.moveCalculation = WaitForMove(self.bot, self.board)
        self.moveCalculation.done.connect(self.makeBotMove)
        self.moveCalculation.error.connect(self.botMoveError)
        self.moveCalculation.start()

    def buttonClick(self):
        self.qBoard.setClickEnabled(False)
        button = self.sender()
        print(button.id)
        px, py = button.id // 9, button.id % 9
        try:
            self.board.make_move(px, py)
        except game.boards.IllegalMoveError as err:
            print(err)
            self.qBoard.setClickEnabled(True)
            return
        except game.boards.GameEndedError as err:
            print(err)
            return
        self.qBoard.updateBoard(self.board)

        self.botMove()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QSinglePlayerGame(True)
    window.show()
    sys.exit(app.exec_())
