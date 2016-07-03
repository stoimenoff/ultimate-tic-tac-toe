from . import SinglePlayerGame
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QFileDialog,
                             QStackedWidget, QGroupBox, QRadioButton, QSpinBox,
                             QHBoxLayout, QLabel)
import pickle


class SinglePlayerMenu(QWidget):
    def __init__(self):
        super(SinglePlayerMenu, self).__init__()
        self.startButton = QPushButton('Start new game')
        self.loadButton = QPushButton('Load saved game')
        self.difficultyMenu = self.createDifficultyMenu()
        self.numberOfGamesSpinBox = QSpinBox()
        self.numberOfGamesSpinBox.setRange(1, 19)
        self.numberOfGamesSpinBox.setFixedWidth(50)
        spinBoxLayout = QHBoxLayout()
        spinBoxLayout.addWidget(QLabel('Number of games'))
        spinBoxLayout.addWidget(self.numberOfGamesSpinBox)
        layout = QVBoxLayout()
        layout.addWidget(self.difficultyMenu)
        layout.addLayout(spinBoxLayout)
        layout.addWidget(self.startButton)
        layout.addWidget(self.loadButton)
        self.setLayout(layout)

    def createDifficultyMenu(self):
        groupBox = QGroupBox("Difficulty")

        choice1 = self.createRadio("&Diff 1", 1)
        choice2 = self.createRadio("D&iff 2", 2)
        choice3 = self.createRadio("Di&ff 3", 3)
        choice4 = self.createRadio("Di&ff 4", 4)

        choice1.setChecked(True)
        self.difficultySelected = 1

        vbox = QVBoxLayout()
        vbox.addWidget(choice1)
        vbox.addWidget(choice2)
        vbox.addWidget(choice3)
        vbox.addWidget(choice4)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        return groupBox

    def createRadio(self, text, id):
        choice = QRadioButton(text)
        choice.id = id
        choice.clicked.connect(self.difficultyChange)
        return choice

    def difficultyChange(self):
        self.difficultySelected = self.sender().id


class SinglePlayer(QWidget):
    def __init__(self):
        super(SinglePlayer, self).__init__()
        self.exitButton = QPushButton('Exit to menu')
        self.game = None
        self.gameMenu = SinglePlayerMenu()
        self.gameMenu.startButton.clicked.connect(self.startGame)
        self.gameMenu.loadButton.clicked.connect(self.loadGame)

        self.stack = QStackedWidget()
        self.stack.addWidget(self.gameMenu)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        layout.addWidget(self.exitButton)

        self.setLayout(layout)

    def startGame(self):
        difficulty = self.gameMenu.difficultySelected
        numberOfGames = self.gameMenu.numberOfGamesSpinBox.value()
        self.game = SinglePlayerGame(difficulty, numberOfGames)
        self.showGame()

    def loadGame(self):
        filename = QFileDialog().getOpenFileName(self, 'Load game')
        if not filename[0]:
            return
        with open(filename[0], 'rb') as handle:
            config = pickle.load(handle)
        self.game = SinglePlayerGame()
        self.game.loadConfiguration(config)
        self.showGame()

    def showGame(self):
        self.stack.addWidget(self.game)
        self.stack.setCurrentWidget(self.game)
