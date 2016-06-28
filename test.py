import sys
from gui import *
import game
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
import time


class QGame(QWidget):
    def __init__(self):
        super(QGame, self).__init__()
        # self.bot = game.players.ai.RandomBot('Bot')
        self.bot = game.players.ai.EuristicsBot('Bot')
        self.board = game.boards.Macroboard()
        layout = QVBoxLayout()
        layout.addWidget(QMacroBoard(self.buttonClick))
        self.setLayout(layout)

    @property
    def qBoard(self):
        return self.layout().itemAt(0).widget()

    def buttonClick(self):
        self.qBoard.setClickEnabled(False)
        button = self.sender()
        print(button.id)
        px, py = button.id // 9, button.id % 9
        try:
            self.board.make_move(px, py)
        except game.boards.IllegalMoveError as err:
            print(err)
            self.qBoard.setClickEnabled(True)
            return

        self.qBoard.updateBoard(self.board)

        try:
            time.sleep(2)
            move = self.bot.choose_move(self.board)
            self.board.make_move(*move)
        except game.boards.IllegalMoveError as err:
            print(err)
        except:  # TODO implmemnet GameEndedError
            print('Bot move failed')

        self.qBoard.updateBoard(self.board)
        self.qBoard.setClickEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QGame()
    window.show()
    sys.exit(app.exec_())
