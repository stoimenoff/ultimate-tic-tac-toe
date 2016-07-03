from ultimatetictactoe.gui.multiplayer import ClientGame
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = ClientGame()
    window.move(50, 50)
    window.show()
    sys.exit(app.exec_())
