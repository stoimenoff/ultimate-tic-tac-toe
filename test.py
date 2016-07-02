import sys
from gui import *
from gui.hotseatgame import HotSeatGame
from gui.singleplayer import SinglePlayer
from gui.multiplayer import MultiPlayerMenu, MultiPlayer
from gui.multiplayerserver import ServerGame
from PyQt5.QtWidgets import QApplication
# import pickle


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # window = SinglePlayerGame(1, 1)
    # window = SinglePlayer()
    # window = HotSeatGame()
    # window = ServerGame()
    window = MultiPlayer()
    window.move(50, 50)
    window.show()
    sys.exit(app.exec_())
