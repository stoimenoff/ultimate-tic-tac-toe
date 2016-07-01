import sys
from gui import *
from gui.multiplayerclient import ClientGame
from PyQt5.QtWidgets import QApplication
# import pickle


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # window = SinglePlayerGame(1, 1)
    # window = SinglePlayer()
    # window = HotSeatGame()
    window = ClientGame()
    window.move(50, 50)
    window.show()
    sys.exit(app.exec_())
