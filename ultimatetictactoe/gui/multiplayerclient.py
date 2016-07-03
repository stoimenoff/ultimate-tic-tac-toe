from .. import game
from .qboards import QMacroBoard
from .qgame import WaitForMove
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QWidget)


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

    def setServerAddress(self, host, port):
        self.opponent.set_target(host, port)

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

    def opponentMove(self, makeMove=True):
        self.moveCalculation = WaitForMove(self.opponent, self.board)
        if makeMove:
            self.moveCalculation.done.connect(self.makeOpponentMove)
        self.moveCalculation.error.connect(self.serverError)
        self.moveCalculation.start()

    def makeOpponentMove(self, px, py):
        try:
            self.board.make_move(px, py)
        except game.boards.IllegalMoveError as err:
            print(err)
            return
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

    def displayMessage(self, msg):
        self.statusBar.setText(msg)
        self.statusBar.show()
