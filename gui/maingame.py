from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton,
                             QStackedWidget, QHBoxLayout, QLabel,
                             QApplication)
from PyQt5.QtGui import QFont


class MainGameMenu(QWidget):
    def __init__(self):
        super(MainGameMenu, self).__init__()
        self.singlePlayerButton = QPushButton('Single player')
        self.multiPlayerButton = QPushButton('Multi player')
        self.spectateButton = QPushButton('Watch BOT battle')
        self.exitButton = QPushButton('Exit game')
        self.exitButton.clicked.connect(QApplication.instance().quit)

        mainLayout = QVBoxLayout()
        self.title = self.createTitleLabel('Ultimate tic-tac-toe')
        mainLayout.addLayout(self.createMenuItem(self.title))
        mainLayout.addLayout(self.createMenuItem(self.singlePlayerButton))
        mainLayout.addLayout(self.createMenuItem(self.multiPlayerButton))
        mainLayout.addLayout(self.createMenuItem(self.spectateButton))
        mainLayout.addLayout(self.createMenuItem(self.exitButton))
        self.setLayout(mainLayout)
        self.setWindowTitle('Ultimate tic-tac-toe')
        self.resize(400, 200)

    def createTitleLabel(self, title):
        titleLabel = QLabel(title)
        font = QFont()
        font.setBold(True)
        font.setPointSize(18)
        titleLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        titleLabel.setFont(font)
        return titleLabel

    def createMenuItem(self, button):
        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(button)
        layout.addStretch(1)
        return layout
