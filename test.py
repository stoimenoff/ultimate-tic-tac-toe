import sys
from gui import *
from gui.hotseatgame import HotSeatGame
from gui.singleplayer import SinglePlayer
from gui.multiplayerserver import ServerGame
from PyQt5.QtWidgets import QApplication
# import pickle


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # window = SinglePlayerGame(1, 1)
    # window = SinglePlayer()
    # window = HotSeatGame()
    window = ServerGame()
    window.move(0, 0)
    window.show()
    sys.exit(app.exec_())
