from .. import game
from . import QMacroBoard
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal


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
        except Exception as e:
            print('error ', e)
            self.error.emit(e)
            return
        print('Move')
        self.done.emit(*move)


class QGame(QWidget):
    gameEnded = pyqtSignal()

    def __init__(self, secondPlayer, humanIsNotFirst=False):
        super(QGame, self).__init__()
        layout = QVBoxLayout()
        self.qBoard = QMacroBoard(self.buttonClick)
        layout.addWidget(self.qBoard)
        self.setLayout(layout)

        self.initGame(humanIsNotFirst, secondPlayer)

    def initGame(self, humanIsNotFirst, secondPlayer):
        self.qBoard.setClickEnabled(True)
        self.bot = secondPlayer
        self.board = game.boards.Macroboard(not humanIsNotFirst)
        if humanIsNotFirst:
            self.qBoard.setClickEnabled(False)
            self.botMove()
        self.qBoard.updateBoard(self.board)

    def reset(self, humanIsNotFirst):
        self.initGame(humanIsNotFirst, self.bot)

    def makeBotMove(self, px, py):
        self.board.make_move(px, py)
        self.qBoard.updateBoard(self.board)
        if self.board.state != game.boards.State.IN_PROGRESS:
            self.gameEnded.emit()
            return
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
        px, py = button.id // 9, button.id % 9
        try:
            self.board.make_move(px, py)
        except game.boards.IllegalMoveError as err:
            print(err)
            self.qBoard.setClickEnabled(True)
            return

        self.qBoard.updateBoard(self.board)

        if self.board.state != game.boards.State.IN_PROGRESS:
            self.gameEnded.emit()
            return

        self.botMove()

    def loadBoard(self, board):
        self.board = board
        self.qBoard.updateBoard(self.board)

    def setSecondPlayer(self, secondPlayer):
        self.bot = secondPlayer
