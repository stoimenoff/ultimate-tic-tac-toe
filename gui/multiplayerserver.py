import game
from . import QMacroBoard
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel,
                             QMessageBox, QPushButton, QVBoxLayout, QWidget)
from PyQt5.QtCore import QThread, pyqtSignal


class WaitForRequest(QThread):
    done = pyqtSignal()
    error = pyqtSignal(Exception)

    def __init__(self, server):
        super(WaitForRequest, self).__init__()
        self.server = server

    def run(self):
        print('Waiting for request')
        try:
            self.server.listen()
        except Exception as e:
            print('error ', e)
            self.error.emit(e)
            return
        print('Move')
        self.done.emit()


class ServerGame(QWidget):
    clickedButton = pyqtSignal(int)

    def __init__(self, parent=None):
        super(ServerGame, self).__init__(parent)

        layout = QVBoxLayout()
        self.qBoard = QMacroBoard(self.buttonClick)
        layout.addWidget(self.qBoard)
        self.setLayout(layout)

        self.server = game.players.human.ServerPlayer(self.moveRequest)
        self.opponentConnected = False
        self.board = None
        self.waitForRequest()

    def waitForRequest(self):
        self.requestThread = WaitForRequest(self.server)
        # self.requestThread.error.done()
        # self.requestThread.error.connect()
        self.requestThread.start()

    def onButtonClick(self):
        button = self.sender()
        self.clickedButton.emit(button.id)

    def moveRequest(self, name, macroboard):
        if not self.opponentConnected:
            print('First connection')
            self.opponentConnected = True
        move = (0, 0)
        return move
