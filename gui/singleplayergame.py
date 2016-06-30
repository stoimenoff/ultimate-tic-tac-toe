import game
from . import QGame
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton,
                             QLabel, QLCDNumber, QFileDialog)
import time
import pickle


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

        layout = QGridLayout()
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        self.scoreLabel = QLabel('Score: ')

        self.gameWidget = QGame(self.getOpponent())
        self.gameWidget.gameEnded.connect(self.updateScoreAndReset)
        self.saveButton = QPushButton('Save game')
        self.saveButton.clicked.connect(self.saveGame)
        self.exitButton = QPushButton('Exit to menu')
        self.message = self.createLabel('')
        self.message.hide()
        layout.addWidget(self.createLabel('You'), 0, 0)
        layout.addWidget(self.createLabel('Opponent'), 0, 1)
        layout.addWidget(self.playerScoreLcd, 1, 0)
        layout.addWidget(self.opponentScoreLcd, 1, 1)
        layout.addWidget(self.gameWidget, 2, 0, 1, 2)
        layout.addWidget(self.gamesCounter, 3, 0)
        layout.addWidget(self.exitButton, 3, 1)
        layout.addWidget(self.saveButton, 4, 1)
        layout.addWidget(self.message, 5, 0, 1, 2)
        self.setLayout(layout)
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

    def saveGame(self):
        filename = QFileDialog().getSaveFileName(self, 'Save game',
                                                 'untitledgame')
        if not filename[0]:
            return
        self.message.setText('Saving...')
        self.message.show()
        with open(filename[0], 'wb') as handle:
            pickle.dump(self.getConfiguration(), handle)
        self.message.setText('Saved!')
        self.message.show()

    def getConfiguration(self):
        return (self.difficulty,
                self.numberOfGames,
                self.gamesPlayed,
                self.playerScore,
                self.opponentScore,
                self.playerIsNotFirst,
                self.gameWidget.board)

    def loadConfiguration(self, config):
        self.difficulty = config[0]
        self.numberOfGames = config[1]
        self.gamesPlayed = config[2]
        self.playerScore = config[3]
        self.opponentScore = config[4]
        self.playerIsNotFirst = config[5]
        self.gameWidget.loadBoard(config[6])
        self.gameWidget.setSecondPlayer(self.getOpponent())
