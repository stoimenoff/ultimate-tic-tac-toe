from .. import game
from . import QMacroBoard
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
                             QLabel)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtCore import Qt
import datetime
import time


DEFAULT_TIME = 1


class MoveThread(QThread):
    calculated = pyqtSignal(int, int)

    def __init__(self, bot, board, minimumTime=DEFAULT_TIME):
        super(MoveThread, self).__init__()
        self.bot = bot
        self.board = board
        self.minimumTime = minimumTime

    def run(self):
        start = datetime.datetime.now()
        move = self.bot.choose_move(self.board)
        delta = datetime.datetime.now() - start
        timeLeft = self.minimumTime - delta.total_seconds()
        if timeLeft > 0:
            time.sleep(timeLeft)
        self.calculated.emit(*move)


class BotBattle(QWidget):

    def __init__(self, bot1, bot2):
        super(BotBattle, self).__init__()
        self.bot1 = bot1
        self.bot2 = bot2
        self.on_turn = self.bot1
        self.board = game.boards.Macroboard()
        self.qBoard = QMacroBoard(self.buttonClick)
        self.qBoard.setClickEnabled(False)
        self.qBoard.updateBoard(self.board)

        button = self.createButton()
        layout = QVBoxLayout()
        layout.addWidget(self.createTitle())
        layout.addWidget(self.qBoard)
        layout.addLayout(button)
        self.setLayout(layout)

    def botMove(self):
        self.moveCalculation = MoveThread(self.on_turn, self.board)
        self.moveCalculation.calculated.connect(self.makeBotMove)
        self.moveCalculation.start()

    def makeBotMove(self, px, py):
        self.board.make_move(px, py)
        self.on_turn = self.bot1 if self.on_turn == self.bot2 else self.bot2
        self.qBoard.updateBoard(self.board)
        if self.board.state != game.boards.State.IN_PROGRESS:
            self.startButton.show()
            return
        self.botMove()

    def createTitle(self):
        title = QLabel(self.bot1.name + ' vs ' + self.bot2.name)
        font = QFont()
        font.setBold(True)
        font.setPointSize(12)
        title.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        title.setFont(font)
        return title

    def createButton(self):
        self.startButton = QPushButton('Start')
        self.startButton.clicked.connect(self.start)
        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.startButton)
        layout.addStretch(1)
        return layout

    def start(self):
        self.startButton.hide()
        self.board = game.boards.Macroboard()
        self.qBoard.updateBoard(self.board)
        self.botMove()

    def buttonClick(self):
        return
