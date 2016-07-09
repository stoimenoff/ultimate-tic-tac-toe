from ... import game
from ...game.players.human.onlineplayer import BadRequestError
from ..qboards import QMacroBoard
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QWidget)
from PyQt5.QtCore import QThread, pyqtSignal, QMutex, QWaitCondition


class RequestHandler(QObject):
    """
    Worker object for handling requests.
    """
    waitingRequest = pyqtSignal()
    requestAccepted = pyqtSignal()
    error = pyqtSignal(Exception)
    terminated = pyqtSignal()

    def __init__(self, parent):
        super(RequestHandler, self).__init__()
        self.parent = parent
        self.__terminated = False
        self.mutex = QMutex()
        self.waitForClick = QWaitCondition()

    def run(self):
        """
        Uses parent's server to listen for request.

        When a valid request is handled, emits requestAccepted singal
        and waits on Mutex condition.
        The parent should wake the worker when a click is made
        via wakeOnClick() method.
        When woken respond to the request with the click that was made.

        Can be terminated from the parent.

        Listening ignores bad requests.
        If OSError occurres, terminates itself and emits error signal.

        On termination emits the terminate signal.
        """
        # print('run')
        self.__terminated = False
        while not self.__terminated:
            # print('Waiting for request')
            self.waitingRequest.emit()
            try:
                self.parent.server.listen(self.onMoveRequest)
            except OSError as e:
                print('error ', e)
                self.error.emit(e)
                self.__terminated = True
            except BadRequestError as e:
                print(e)
                continue
        print('Worker terminated')
        self.terminated.emit()

    def onMoveRequest(self, name, macroboard):
        if self.__terminated:
            return None
        self.opponentName = name
        self.macroboard = macroboard
        self.requestAccepted.emit()
        self.__sleepUntilClick()
        if self.__terminated:
            return None
        move = self.parent.last_click
        return move

    def __sleepUntilClick(self):
        self.mutex.lock()
        self.waitForClick.wait(self.mutex)
        self.mutex.unlock()

    def wakeOnClick(self):
        self.mutex.lock()
        self.waitForClick.wakeOne()
        self.mutex.unlock()

    def terminate(self):
        """
        Terminates the worker.
        """
        if self.__terminated:
            return
        self.__terminated = True
        self.wakeOnClick()
        self.parent.server.stop()


class ServerGame(QWidget):
    def __init__(self, name, port, parent=None):
        super(ServerGame, self).__init__(parent)

        self.qBoard = QMacroBoard(self.onButtonClick)
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

        self.server = game.players.human.ServerPlayer(name, port)
        self.opponentConnected = False
        self.board = None
        self.last_click = None
        self.qBoard.updateBoard(game.boards.Macroboard())
        self.qBoard.setClickEnabled(False)

        self.requestThread = QThread()

        self.requestWorker = RequestHandler(self)
        self.requestWorker.waitingRequest.connect(self.waitingOpponentMessage)
        self.requestWorker.requestAccepted.connect(self.moveRequest)
        self.requestWorker.error.connect(self.serverError)
        self.requestWorker.moveToThread(self.requestThread)
        self.requestThread.started.connect(self.requestWorker.run)
        self.requestWorker.terminated.connect(self.requestThread.quit)

        self.requestThread.start()

    def __del__(self):
        self.requestWorker.terminate()
        self.requestThread.wait()

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
        self.requestWorker.wakeOnClick()

    def moveRequest(self):
        if not self.opponentConnected:
            self.displayMessage(self.requestWorker.opponentName +
                                ' connected to you! Game on!')
            self.titleBar.setText('Game against ' +
                                  self.requestWorker.opponentName)
            self.titleBar.show()
            self.opponentConnected = True
        else:
            self.displayMessage('Your turn!')
        self.board = self.requestWorker.macroboard
        if self.board.state == game.boards.State.IN_PROGRESS:
            self.qBoard.setClickEnabled(True)
        else:
            self.announceGameResult()
            self.requestWorker.terminate()
        self.qBoard.updateBoard(self.board)

    def serverError(self, err):
        print('Server error:', err)
        self.displayMessage('Server err: ' + str(err))

    def displayMessage(self, msg):
        self.statusBar.setText(msg)
        self.statusBar.show()

    def waitingOpponentMessage(self):
        if not self.opponentConnected:
            self.displayMessage('Waiting opponent to connect.')
        else:
            self.displayMessage('Waiting opponent to play.')

    def announceGameResult(self):
        message = ''
        result = self.board.state
        if result == game.boards.State.O_WON:
            message = 'Congrats! You won the game!'
        elif result == game.boards.State.X_WON:
            message = 'Sorry! You lost the game!'
        elif result == game.boards.State.DRAW:
            message = 'The game ended in a draw!'
        self.displayMessage(message)

    def end(self):
        self.requestWorker.terminate()
