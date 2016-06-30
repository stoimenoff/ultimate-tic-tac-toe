import sys
from gui import *
from gui.singleplayergame import SinglePlayerGame
from PyQt5.QtWidgets import QApplication
# import pickle


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SinglePlayerGame(1, 1)
    window.show()
    sys.exit(app.exec_())
