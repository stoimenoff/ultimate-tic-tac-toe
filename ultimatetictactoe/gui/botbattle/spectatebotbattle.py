from ... import game
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton,
                             QStackedWidget, QHBoxLayout, QGroupBox,
                             QRadioButton)
from .botbattle import BotBattle


class BotBattleMenu(QWidget):
    def __init__(self):
        super(BotBattleMenu, self).__init__()

        self.bot1Level = 1
        self.bot2Level = 1
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(self.createBotSelectors())
        mainLayout.addLayout(self.createStart())
        self.setLayout(mainLayout)

    def createBotSelectors(self):
        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.createBotSelector('Bot 1 level',
                         self.bot1LevelChange))
        layout.addStretch(1)
        layout.addWidget(self.createBotSelector('Bot 2 level',
                         self.bot2LevelChange))
        layout.addStretch(1)
        return layout

    def createBotSelector(self, title, onClick):
        groupBox = QGroupBox(title)

        choice1 = self.createRadio("&Diff 1", 1, onClick)
        choice2 = self.createRadio("D&iff 2", 2, onClick)
        choice3 = self.createRadio("Di&ff 3", 3, onClick)
        choice4 = self.createRadio("Di&ff 4", 4, onClick)

        choice1.setChecked(True)

        vbox = QVBoxLayout()
        vbox.addWidget(choice1)
        vbox.addWidget(choice2)
        vbox.addWidget(choice3)
        vbox.addWidget(choice4)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        return groupBox

    def createStart(self):
        self.startButton = QPushButton('Start battle')
        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.startButton)
        layout.addStretch(1)
        return layout

    def createRadio(self, text, id, onClick):
        choice = QRadioButton(text)
        choice.id = id
        choice.clicked.connect(onClick)
        return choice

    def bot1LevelChange(self):
        self.bot1Level = self.sender().id

    def bot2LevelChange(self):
        self.bot2Level = self.sender().id


class SpectateBattle(QWidget):
    def __init__(self):
        super(SpectateBattle, self).__init__()
        self.exitButton = QPushButton('Exit to menu')
        self.exitButton.clicked.connect(self.interruptBattle)
        self.menu = BotBattleMenu()
        self.menu.startButton.clicked.connect(self.startBattle)
        self.battle = None

        self.stack = QStackedWidget()
        self.stack.addWidget(self.menu)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        layout.addWidget(self.exitButton)
        self.setLayout(layout)

    def startBattle(self):
        bot1 = game.players.ai.select_bot(self.menu.bot1Level)
        bot2 = game.players.ai.select_bot(self.menu.bot2Level)
        self.battle = BotBattle(bot1, bot2)
        self.stack.addWidget(self.battle)
        self.stack.setCurrentWidget(self.battle)

    def interruptBattle(self):
        if self.battle:
            self.battle.interrupt()
