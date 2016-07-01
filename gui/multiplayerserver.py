import game
from . import QMacroBoard
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel,
                             QMessageBox, QPushButton, QVBoxLayout, QWidget)
from PyQt5.QtCore import QThread, pyqtSignal, QMutex, QWaitCondition


class WaitForRequest(QThread):
    requestHandled = pyqtSignal()
    moveRequested = pyqtSignal()
    error = pyqtSignal(Exception)

    def __init__(self, parent):
        super(WaitForRequest, self).__init__()
        self.parent = parent
        self.listen = True

    def run(self):
        while self.listen:
            print('Waiting for request')
            try:
                self.parent.server.listen(self.onMoveRequest)
            except Exception as e:
                print('error ', e)
                self.error.emit(e)
                return
            self.requestHandled.emit()

    def onMoveRequest(self, name, macroboard):
        # self.parent.moveRequest(name, macroboard)
        self.opponentName = name
        self.macroboard = macroboard
        self.moveRequested.emit()
        print('asd')
        self.parent.mutex.lock()
        self.parent.waitForClick.wait(self.parent.mutex)
        move = self.parent.last_click
        self.parent.mutex.unlock()
        return move


class ServerGame(QWidget):
    def __init__(self, parent=None):
        super(ServerGame, self).__init__(parent)

        layout = QVBoxLayout()
        self.qBoard = QMacroBoard(self.onButtonClick)
        layout.addWidget(self.qBoard)
        self.setLayout(layout)

        self.server = game.players.human.ServerPlayer()
        self.opponentConnected = False
        self.board = None
        self.last_click = None
        self.qBoard.setClickEnabled(False)

        self.mutex = QMutex()
        self.waitForClick = QWaitCondition()
        self.waitForRequest()

    def waitForRequest(self):
        self.requestThread = WaitForRequest(self)
        self.requestThread.moveRequested.connect(self.moveRequest)
        # self.requestThread.requestHandled.connect(self.waitForRequest)
        self.requestThread.error.connect(self.serverError)
        self.requestThread.start()

    def onButtonClick(self):
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
        self.last_click = (px, py)
        self.mutex.lock()
        self.waitForClick.wakeOne()
        self.mutex.unlock()

    def moveRequest(self):
        if not self.opponentConnected:
            print('First connection')
            self.opponentConnected = True
        self.board = self.requestThread.macroboard
        self.qBoard.setClickEnabled(True)
        self.qBoard.updateBoard(self.board)

    def serverError(self, err):
        print('Server error:', err)
