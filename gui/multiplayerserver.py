import game
from . import QMacroBoard
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QWidget)
from PyQt5.QtCore import QThread, pyqtSignal, QMutex, QWaitCondition


class WaitForRequest(QThread):
    waitingRequest = pyqtSignal()
    requestHandled = pyqtSignal()
    requestAccepted = pyqtSignal()
    error = pyqtSignal(Exception)

    def __init__(self, parent):
        super(WaitForRequest, self).__init__()
        self.parent = parent
        self.listen = True

    def run(self):
        while self.listen:
            print('Waiting for request')
            self.waitingRequest.emit()
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
        self.requestAccepted.emit()
        self.parent.mutex.lock()
        self.parent.waitForClick.wait(self.parent.mutex)
        move = self.parent.last_click
        self.parent.mutex.unlock()
        return move


class ServerGame(QWidget):
    def __init__(self, parent=None):
        super(ServerGame, self).__init__(parent)

        self.qBoard = QMacroBoard(self.onButtonClick)
        self.statusBar = QLabel()
        self.statusBar.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.statusBar.hide()
        layout = QVBoxLayout()
        layout.addWidget(self.qBoard)
        layout.addWidget(self.statusBar)
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
        self.requestThread.waitingRequest.connect(self.waitingOpponentMessage)
        self.requestThread.requestAccepted.connect(self.moveRequest)
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
            self.displayMessage(self.requestThread.opponentName +
                                ' connected to you! Game on!')
            self.opponentConnected = True
        else:
            self.displayMessage('Your turn!')
        self.board = self.requestThread.macroboard
        if self.board.state == game.boards.State.IN_PROGRESS:
            self.qBoard.setClickEnabled(True)
        else:
            self.displayMessage('Game ended!')
            # release waiting thread
            self.requestThread.listen = False
            self.mutex.lock()
            self.waitForClick.wakeOne()
            self.mutex.unlock()
        self.qBoard.updateBoard(self.board)

    def serverError(self, err):
        print('Server error:', err)

    def displayMessage(self, msg):
        self.statusBar.setText(msg)
        self.statusBar.show()

    def waitingOpponentMessage(self):
        if not self.opponentConnected:
            self.displayMessage('Waiting opponent to connect.')
        else:
            self.displayMessage('Waiting opponent to play.')
