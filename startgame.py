from ultimatetictactoe.gui import MainGame
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainGame()
    window.move(50, 50)
    window.show()
    sys.exit(app.exec_())
