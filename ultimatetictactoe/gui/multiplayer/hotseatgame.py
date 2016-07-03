from ... import game
from ..qboards import QMacroBoard
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSignal


class HotSeatGame(QWidget):

    gameEnded = pyqtSignal()

    def __init__(self):
        super(HotSeatGame, self).__init__()
        layout = QVBoxLayout()
        self.qBoard = QMacroBoard(self.buttonClick)
        layout.addWidget(self.qBoard)
        self.setLayout(layout)
        self.board = game.boards.Macroboard()
        self.qBoard.updateBoard(self.board)

    def buttonClick(self):
        button = self.sender()
        px, py = button.id // 9, button.id % 9
        try:
            self.board.make_move(px, py)
        except game.boards.IllegalMoveError as err:
            print(err)
            return
        except game.boards.GameEndedError as err:
            print(err)
            self.gameEnded.emit()
            return

        self.qBoard.updateBoard(self.board)

    def loadBoard(self, board):
        self.board = board
        self.qBoard.updateBoard(self.board)
