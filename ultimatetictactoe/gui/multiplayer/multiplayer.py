from PyQt5.QtCore import Qt
from PyQt5.QtNetwork import QHostAddress
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton,
                             QStackedWidget, QSpinBox, QHBoxLayout, QLabel,
                             QLineEdit, QFrame, QGridLayout)
from .multiplayerclient import ClientGame
from .multiplayerserver import ServerGame
from .hotseatgame import HotSeatGame


class MultiPlayerMenu(QWidget):
    def __init__(self):
        super(MultiPlayerMenu, self).__init__()
        nameLayout = self.createNameField()
        networkConfig = self.createIpAndPortFields()
        networkButtons = self.createConnectAndHostButtons()

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.createTitleLabel('Online'))
        mainLayout.addLayout(nameLayout)
        mainLayout.addLayout(networkConfig)
        mainLayout.addLayout(networkButtons)
        mainLayout.addWidget(self.createHorizontalLine())
        mainLayout.addWidget(self.createTitleLabel('Hotseat on one PC'))
        mainLayout.addWidget(self.createHotseatButton())
        self.setLayout(mainLayout)

    def createNameField(self):
        self.nameLabel = QLabel('Your name: ')
        self.nameField = QLineEdit()
        self.nameField.setMaxLength(20)
        self.nameField.textChanged.connect(self.nameChange)
        layout = QHBoxLayout()
        layout.addWidget(self.nameLabel)
        layout.addWidget(self.nameField)
        return layout

    def createIpAndPortFields(self):
        ipLabel = QLabel('Opponent IP:')
        ipLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        portLabel = QLabel('Game port:')
        portLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.ipField = QLineEdit()
        self.ipField.setInputMask('000.000.000.000; ')
        self.ipField.setFixedWidth(130)
        self.ipField.textChanged.connect(self.ipChange)
        self.portSpinBox = QSpinBox()
        self.portSpinBox.setRange(1024, 8080)
        self.portSpinBox.setFixedWidth(80)
        layout = QGridLayout()
        layout.addWidget(ipLabel, 0, 0)
        layout.addWidget(self.ipField, 0, 1)
        layout.addWidget(portLabel, 1, 0)
        layout.addWidget(self.portSpinBox, 1, 1)
        return layout

    def createConnectAndHostButtons(self):
        self.connectButton = QPushButton('Connect')
        self.connectButton.setEnabled(False)
        self.hostButton = QPushButton('Host game')
        self.hostButton.setEnabled(False)
        layout = QHBoxLayout()
        layout.addWidget(self.connectButton)
        layout.addWidget(self.hostButton)
        return layout

    def createTitleLabel(self, title):
        titleLabel = QLabel(title)
        titleLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        return titleLabel

    def createHotseatButton(self):
        self.hotseatButton = QPushButton('Play')
        return self.hotseatButton

    def createHorizontalLine(self):
        line = QLabel()
        line.setFrameStyle(QFrame.HLine)
        return line

    def nameChange(self):
        if self.nameIsValid():
            self.hostButton.setEnabled(True)
            if self.ipIsValid():
                self.connectButton.setEnabled(True)
        else:
            self.hostButton.setEnabled(False)
            self.connectButton.setEnabled(False)

    def ipChange(self):
        if self.ipIsValid():
            if self.nameIsValid():
                self.connectButton.setEnabled(True)
        else:
            self.connectButton.setEnabled(False)

    def ipIsValid(self):
        return QHostAddress().setAddress(self.ipField.text())

    def nameIsValid(self):
        if self.nameField.text():
            return True
        return False


class MultiPlayer(QWidget):
    def __init__(self):
        super(MultiPlayer, self).__init__()
        self.exitButton = QPushButton('Exit to menu')
        self.exitButton.clicked.connect(self.exit)
        self.menu = MultiPlayerMenu()
        self.menu.connectButton.clicked.connect(self.connect)
        self.menu.hostButton.clicked.connect(self.host)
        self.menu.hotseatButton.clicked.connect(self.hotseat)

        self.stack = QStackedWidget()
        self.stack.addWidget(self.menu)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        layout.addWidget(self.exitButton)

        self.setLayout(layout)
        self.clientGame = None
        self.serverGame = None
        self.hotseatGame = None

    def host(self):
        name = self.menu.nameField.text()
        port = self.menu.portSpinBox.value()
        self.serverGame = ServerGame(name, port)
        self.showGame(self.serverGame)

    def connect(self):
        name = self.menu.nameField.text()
        ip = self.menu.ipField.text()
        port = self.menu.portSpinBox.value()
        self.clientGame = ClientGame(name, ip, port)
        self.showGame(self.clientGame)

    def hotseat(self):
        self.hotseatGame = HotSeatGame()
        self.showGame(self.hotseatGame)

    def showGame(self, game):
        self.stack.addWidget(game)
        self.stack.setCurrentWidget(game)

    def exit(self):
        self.stack.setCurrentWidget(self.menu)
        if self.serverGame:
            self.serverGame.end()
