import sys
from gui import *
from gui.singleplayergame import SinglePlayerGame
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # window = QGame()
    window = SinglePlayerGame(1, 2)
    window.show()
    sys.exit(app.exec_())
