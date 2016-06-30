import game
from . import QGame
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton,
                             QLabel, QLCDNumber)
import time


class SinglePlayerGame(QWidget):
    def __init__(self, difficulty, numberOfGames):
        super(SinglePlayerGame, self).__init__()
        self.difficulty = difficulty
        self.numberOfGames = numberOfGames
        self.gamesPlayed = 0
        self.playerScore = 0
        self.opponentScore = 0
        self.playerIsNotFirst = False

        self.playerScoreLcd = QLCDNumber(2)
        self.playerScoreLcd.setSegmentStyle(QLCDNumber.Filled)
        self.opponentScoreLcd = QLCDNumber(2)
        self.opponentScoreLcd.setSegmentStyle(QLCDNumber.Filled)

        self.gamesCounter = QLabel()
        self.gamesCounter.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.updateGameCounter()

        layoyt = QGridLayout()
        self.scoreLabel = QLabel('Score: ')

        self.gameWidget = QGame(self.getOpponent())
        self.gameWidget.gameEnded.connect(self.updateScoreAndReset)
        self.exitButton = QPushButton('Exit to menu')
        layoyt.addWidget(self.createLabel('You'), 0, 0)
        layoyt.addWidget(self.createLabel('Opponent'), 0, 1)
        layoyt.addWidget(self.playerScoreLcd, 1, 0)
        layoyt.addWidget(self.opponentScoreLcd, 1, 1)
        layoyt.addWidget(self.gameWidget, 2, 0, 1, 2)
        layoyt.addWidget(self.gamesCounter, 3, 0)
        layoyt.addWidget(self.exitButton, 3, 1)
        self.setLayout(layoyt)
        self.resize(400, 750)

    def updateScoreAndReset(self):
        time.sleep(3)
        self.gamesPlayed += 1
        self.playerIsNotFirst = not self.playerIsNotFirst
        result = self.gameWidget.board.state
        if result == game.boards.State.X_WON:
            self.playerScore += 3
        elif result == game.boards.State.O_WON:
            self.opponentScore += 3
        elif result == game.boards.State.DRAW:
            self.playerScore += 1
            self.opponentScore += 1
        self.playerScoreLcd.display(self.playerScore)
        self.opponentScoreLcd.display(self.opponentScore)
        if self.numberOfGames > self.gamesPlayed:
            self.updateGameCounter()
            self.gameWidget.reset(self.playerIsNotFirst)
        else:
            pass

    def updateGameCounter(self):
        self.gamesCounter.setText('Game ' + str(self.gamesPlayed + 1) +
                                  ' of ' + str(self.numberOfGames))

    def createLabel(self, text):
        lbl = QLabel(text)
        lbl.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        return lbl

    def getOpponent(self):
        if self.difficulty == 0:
            return game.players.ai.EuristicsBot('Bot')
        elif self.difficulty == 1:
            return game.players.ai.EuristicsBot('Bot')
        elif self.difficulty == 2:
            return game.players.ai.EuristicsBot('Bot')
        elif self.difficulty == 3:
            return game.players.ai.EuristicsBot('Bot')
