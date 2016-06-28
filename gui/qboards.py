from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QGridLayout, QPushButton, QWidget,
                             QStyleOption, QStyle)
from PyQt5.QtGui import QPainter

SQUARE_COLORS = {'X': 'blue', 'O': 'red', ' ': 'black'}
BOARD_COLORS = {'X': 'lightblue', 'O': 'lightpink',
                ' ': 'white', '-': 'lightyellow', 'l': 'lightgreen'}


class QMicroBoard(QWidget):
    def __init__(self, row, column, onButtonClick, SIZE=3):
        super(QMicroBoard, self).__init__()
        self.SIZE = SIZE
        self.row = row
        self.column = column
        self.onButtonClick = onButtonClick
        grid = QGridLayout()
        for i in range(SIZE):
            for j in range(SIZE):
                sqr = Square(row * SIZE**3 + i * SIZE**2 + column * SIZE + j)
                # sqr = Square((row, column, i, j))
                # sqr = Square((row * SIZE + column, i * SIZE + j))
                sqr.clicked.connect(self.onButtonClick)
                grid.addWidget(sqr, i, j)
        grid.setSpacing(5)
        grid.setVerticalSpacing(5)
        self.setLayout(grid)
        self.lightUp()

    def changeBgColor(self, color):
        self.setStyleSheet('background-color:' + color)

    def lightUp(self):
        self.changeBgColor(BOARD_COLORS['l'])

    def lightDown(self):
        self.changeBgColor(BOARD_COLORS[' '])

    def updateBoard(self, microboard):
        for i in range(self.layout().count()):
            square = microboard.grid[i // self.SIZE][i % self.SIZE]
            button = self.layout().itemAt(i).widget()
            button.setText(square.value)
            button.changeFontColor(SQUARE_COLORS[square.value])

    def setClickEnabled(self, enabled):
        for i in range(self.layout().count()):
            self.layout().itemAt(i).widget().setEnabled(enabled)

    def paintEvent(self, pe):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        s = self.style()
        s.drawPrimitive(QStyle.PE_Widget, opt, p, self)


class QMacroBoard(QWidget):
    def __init__(self, onButtonClick, SIZE=3):
        super(QMacroBoard, self).__init__()
        self.SIZE = SIZE
        self.onButtonClick = onButtonClick
        grid = QGridLayout()
        for i in range(SIZE):
            for j in range(SIZE):
                grid.addWidget(QMicroBoard(i, j, self.onButtonClick,
                               self.SIZE), i, j)
        grid.setSpacing(0)
        grid.setVerticalSpacing(0)
        self.setLayout(grid)

    def updateBoard(self, macroboard):
        for i in range(self.layout().count()):
            microboard = macroboard.boards[i // self.SIZE][i % self.SIZE]
            self.layout().itemAt(i).widget().lightDown()
            self.layout().itemAt(i).widget().updateBoard(microboard)
        for (i, j) in macroboard.available_boards:
            self.layout().itemAt(i * self.SIZE + j).widget().lightUp()
        for (i, j) in macroboard.dead_boards:
            state = macroboard.boards[i][j].state
            board = self.layout().itemAt(i * self.SIZE + j).widget()
            board.changeBgColor(BOARD_COLORS[state.value])
        self.repaint()

    def setClickEnabled(self, enabled):
        for i in range(self.layout().count()):
            self.layout().itemAt(i).widget().setClickEnabled(enabled)


SHEET = '''
        border: 1px solid black;
        width: 50px;
        height: 50px;
        font-size: 50px;
'''


class Square(QPushButton):
    def __init__(self, id, text='&', parent=None):
        super(Square, self).__init__(text, parent)
        self.id = id
        self.setStyleSheet(SHEET)
        self.setFocusPolicy(Qt.NoFocus)

    def changeFontColor(self, color):
        self.setStyleSheet(SHEET + 'color: ' + color)
