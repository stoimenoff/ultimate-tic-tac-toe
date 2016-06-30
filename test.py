import sys
from gui import *
from gui.singleplayergame import SinglePlayerGame
from PyQt5.QtWidgets import QApplication
import pickle


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SinglePlayerGame(1, 3)
    with open('t1', 'rb') as handle:
        config = pickle.load(handle)
    window.loadConfiguration(config)
    window.show()
    sys.exit(app.exec_())
