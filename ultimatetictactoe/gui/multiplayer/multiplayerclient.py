from ... import game
from ..qboards import QMacroBoard
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QWidget)
from ...game.players.human.onlineplayer import (BadRequestError,
                                                BadResponseError)
from PyQt5.QtCore import QThread, pyqtSignal


class MoveRequestMaker(QObject):
    requestMade = pyqtSignal()
    serverResponsed = pyqtSignal(int, int)
    error = pyqtSignal(Exception)
    terminated = pyqtSignal()

    def __init__(self, parent):
        super(MoveRequestMaker, self).__init__()
        self.parent = parent
        self.__terminated = False

    def run(self):
        # print('Making request')
        self.__terminated = False
        self.requestMade.emit()
        try:
            move = self.parent.opponent.choose_move(self.parent.board)
        except (OSError, BadResponseError) as e:
            if not self.__terminated:
                print('error ', e)
                self.error.emit(e)
            return
        if not self.__terminated:
            self.serverResponsed.emit(*move)
        self.terminated.emit()

    def terminate(self):
        self.__terminated = True
        self.parent.opponent.cancel()


class ClientGame(QWidget):
    def __init__(self, name, host, port, parent=None):
        super(ClientGame, self).__init__(parent)

        self.qBoard = QMacroBoard(self.buttonClick)
        self.statusBar = QLabel()
        self.statusBar.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.statusBar.hide()
        self.titleBar = QLabel()
        self.titleBar.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.titleBar.hide()
        layout = QVBoxLayout()
        layout.addWidget(self.titleBar)
        layout.addWidget(self.qBoard)
        layout.addWidget(self.statusBar)
        self.setLayout(layout)

        self.opponent = game.players.human.RemotePlayer(name, host, port)
        self.opponentConnected = False
        self.board = game.boards.Macroboard()
        self.requestMaker = None
        self.requestThread = None

    def __del__(self):
        if self.requestMaker:
            self.requestMaker.terminate()
            self.requestThread.wait()

    def buttonClick(self):
        self.qBoard.setClickEnabled(False)
        button = self.sender()
        px, py = button.id // 9, button.id % 9
        try:
            self.board.make_move(px, py)
        except game.boards.IllegalMoveError as err:
            self.displayMessage(str(err))
            self.qBoard.setClickEnabled(True)
            return
        self.qBoard.updateBoard(self.board)
        if self.board.state != game.boards.State.IN_PROGRESS:
            self.opponentMove(False)
            self.announceGameResult()
            return
        self.displayMessage('Waiting for opponent...')
        self.opponentMove()

    def opponentMove(self):
        self.requestThread = QThread()
        self.requestMaker = MoveRequestMaker(self)
        self.requestMaker.serverResponsed.connect(self.makeOpponentMove)
        self.requestMaker.error.connect(self.serverError)
        self.requestMaker.moveToThread(self.requestThread)
        self.requestThread.started.connect(self.requestMaker.run)
        self.requestMaker.terminated.connect(self.requestThread.quit)
        self.requestThread.start()

    def makeOpponentMove(self, px, py):
        self.board.make_move(px, py)
        self.displayMessage('Your turn.')
        self.titleBar.setText('Game against ' + self.opponent.name)
        self.titleBar.show()
        self.qBoard.updateBoard(self.board)
        if self.board.state != game.boards.State.IN_PROGRESS:
            self.opponentMove(False)
            self.announceGameResult()
            return
        self.qBoard.setClickEnabled(True)

    def announceGameResult(self):
        message = ''
        result = self.board.state
        if result == game.boards.State.X_WON:
            message = 'Congrats! You won the game!'
        elif result == game.boards.State.O_WON:
            message = 'Sorry! You lost the game!'
        elif result == game.boards.State.DRAW:
            message = 'The game ended in a draw!'
        self.displayMessage(message)

    def serverError(self, err):
        print('Server error:', err)
        self.displayMessage('Server err: ' + str(err))

    def displayMessage(self, msg):
        self.statusBar.setText(msg)
        self.statusBar.show()

    def end(self):
        if self.requestMaker:
            self.requestMaker.terminate()
