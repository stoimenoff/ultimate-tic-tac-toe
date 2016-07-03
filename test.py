import sys
from ultimate-tic-tac-toe.gui.
from PyQt5.QtWidgets import QApplication
# import pickle


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # window = SinglePlayerGame(1, 1)
    # window = SinglePlayer()
    # window = HotSeatGame()
    # window = ServerGame()
    # window = MultiPlayer()
    window = MainGame()
    window.move(50, 50)
    window.show()
    sys.exit(app.exec_())
