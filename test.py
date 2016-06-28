import sys
from gui import *
import game
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout


class QGame(QWidget):
    def __init__(self):
        super(QGame, self).__init__()
        # self.bot = game.players.ai.RandomBot('Bot')
        self.bot = game.players.ai.EuristicsBot('Bot')
        self.board = game.boards.Macroboard()
        layout = QVBoxLayout()
        layout.addWidget(QMacroBoard(self.button_click))
        self.setLayout(layout)

    def button_click(self):
        button = self.sender()
        # button.setText('X')
        print(button.id)
        px, py = button.id // 9, button.id % 9
        try:
            self.board.make_move(px, py)
        except game.boards.IllegalMoveError as err:
            print(err)
            return

        move = self.bot.choose_move(self.board)
        self.board.make_move(*move)

        self.layout().itemAt(0).widget().update(self.board)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QGame()
    window.show()
    sys.exit(app.exec_())
