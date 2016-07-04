from ... import game
from .botgame import BotGame
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout,
                             QLabel, QLCDNumber, QFileDialog, QVBoxLayout)
from PyQt5.QtGui import QFont
import time
import pickle


class SinglePlayerGame(QWidget):
    def __init__(self, difficulty=0, numberOfGames=1):
        super(SinglePlayerGame, self).__init__()
        self.difficulty = difficulty
        self.numberOfGames = numberOfGames
        self.gamesPlayed = 0
        self.playerScore = 0
        self.opponentScore = 0
        self.playerIsNotFirst = False

        self.gamesCounter = QLabel()
        self.gamesCounter.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.updateGameCounter()

        mainLayout = QVBoxLayout()

        self.gameWidget = BotGame(self.getOpponent())
        self.gameWidget.gameEnded.connect(self.updateScoreAndReset)
        self.saveButton = QPushButton('Save series')
        self.saveButton.clicked.connect(self.saveGame)
        self.message = self.createLabel('')
        self.message.hide()
        mainLayout.addLayout(self.createScoreLayout())
        mainLayout.addWidget(self.gameWidget)
        mainLayout.addWidget(self.message)
        pack = self.packInHStretch([self.gamesCounter, self.saveButton])
        mainLayout.addLayout(pack)
        self.setLayout(mainLayout)

    def createScoreLayout(self):
        self.playerScoreLcd = QLCDNumber(2)
        self.playerScoreLcd.setSegmentStyle(QLCDNumber.Filled)
        self.playerScoreLcd.setMinimumSize(75, 50)
        self.playerScoreLcd.display(0)
        self.opponentScoreLcd = QLCDNumber(2)
        self.opponentScoreLcd.setSegmentStyle(QLCDNumber.Filled)
        self.opponentScoreLcd.setMinimumSize(75, 50)
        self.opponentScoreLcd.display(0)
        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.createLabel('You: '))
        layout.addWidget(self.playerScoreLcd)
        layout.addStretch(1)
        layout.addWidget(self.createLabel('Opponent: '))
        layout.addWidget(self.opponentScoreLcd)
        layout.addStretch(1)
        return layout

    def packInHStretch(self, widgets):
        layout = QHBoxLayout()
        layout.addStretch(1)
        for widget in widgets:
            layout.addWidget(widget)
            layout.addStretch(1)
        return layout

    def displayMessage(self, message):
        self.message.setText(message)
        self.message.show()
        self.repaint()

    def hideMessage(self):
        self.message.hide()
        self.repaint()

    def updateScoreAndReset(self):
        self.gamesPlayed += 1
        self.playerIsNotFirst = not self.playerIsNotFirst
        result = self.gameWidget.board.state
        message = ''
        if result == game.boards.State.X_WON:
            self.playerScore += 3
            message = 'Congrats! You won the game!'
        elif result == game.boards.State.O_WON:
            self.opponentScore += 3
            message = 'Sorry! You lost the game!'
        elif result == game.boards.State.DRAW:
            self.playerScore += 1
            self.opponentScore += 1
            message = 'The game ended in a draw!'
        self.displayMessage(message)
        self.playerScoreLcd.display(self.playerScore)
        self.opponentScoreLcd.display(self.opponentScore)
        if self.numberOfGames > self.gamesPlayed:
            for i in range(3, 0, -1):
                self.displayMessage(message + ' New game starting in ' +
                                    str(i))
                time.sleep(1)
            self.hideMessage()
            self.gameWidget.reset(self.playerIsNotFirst)
            self.updateGameCounter()
        else:
            self.announceResult()

    def announceResult(self):
        if self.playerScore > self.opponentScore:
            self.displayMessage('Congrats! You won the series!')
        elif self.playerScore < self.opponentScore:
            self.displayMessage('Sorry. You lost the series!')
        else:
            self.displayMessage('The series ended in a draw!')

    def updateGameCounter(self):
        self.gamesCounter.setText('Game ' + str(self.gamesPlayed + 1) +
                                  ' of ' + str(self.numberOfGames))

    def createLabel(self, text):
        lbl = QLabel(text)
        lbl.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        font = QFont()
        font.setPointSize(12)
        lbl.setFont(font)
        return lbl

    def getOpponent(self):
        return game.players.ai.select_bot(self.difficulty)

    def saveGame(self):
        if self.gamesPlayed == self.numberOfGames:
            if self.gameWidget.board.state != game.boards.State.IN_PROGRESS:
                self.displayMessage('Cannot save. The game has ended.')
                return
        filename = QFileDialog().getSaveFileName(self, 'Save game',
                                                 'untitledgame')
        if not filename[0]:
            return
        self.displayMessage('Saving...')
        with open(filename[0], 'wb') as handle:
            pickle.dump(self.getConfiguration(), handle)
        self.displayMessage('Saved!')

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
        self.updateGameCounter()
        self.playerScoreLcd.display(self.playerScore)
        self.opponentScoreLcd.display(self.opponentScore)
