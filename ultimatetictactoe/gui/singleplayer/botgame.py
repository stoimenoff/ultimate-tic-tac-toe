from ... import game
from ..qboards import QMacroBoard
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal, QObject


class WaitForMove(QObject):
    done = pyqtSignal(int, int)
    error = pyqtSignal(Exception)
    terminated = pyqtSignal()

    def __init__(self, player, board):
        super(WaitForMove, self).__init__()
        self.player = player
        self.board = board

    def run(self):
        # print('Waiting for move')
        try:
            move = self.player.choose_move(self.board)
        except (game.boards.GameEndedError, OSError) as e:
            print('error ', e)
            self.error.emit(e)
            return
        # print('Move')
        self.done.emit(*move)
        self.terminated.emit()


class BotGame(QWidget):
    gameEnded = pyqtSignal()

    def __init__(self, secondPlayer, humanIsNotFirst=False):
        super(BotGame, self).__init__()
        layout = QVBoxLayout()
        self.qBoard = QMacroBoard(self.buttonClick)
        layout.addWidget(self.qBoard)
        self.setLayout(layout)

        self.moveThread = None
        self.initGame(humanIsNotFirst, secondPlayer)

    def __del__(self):
        if self.moveThread:
            self.moveThread.wait()

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
        self.moveThread = QThread()
        self.moveCalculation = WaitForMove(self.bot, self.board)
        self.moveCalculation.done.connect(self.makeBotMove)
        self.moveCalculation.error.connect(self.botMoveError)
        self.moveCalculation.moveToThread(self.moveThread)
        self.moveThread.started.connect(self.moveCalculation.run)
        self.moveCalculation.terminated.connect(self.moveThread.quit)
        self.moveThread.start()

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
