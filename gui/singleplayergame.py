import game
from . import QGame
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton,
                             QLabel, QLCDNumber)


class SinglePlayerGame(QWidget):
    def __init__(self, difficulty, numberOfGames):
        super(SinglePlayerGame, self).__init__()
        self.difficulty = difficulty
        self.numberOfGames = numberOfGames
        self.playerScore = 0
        self.opponentScore = 0
        self.playerIsNotFirst = False

        self.playerScoreLcd = QLCDNumber(2)
        self.playerScoreLcd.setSegmentStyle(QLCDNumber.Filled)
        self.opponentScoreLcd = QLCDNumber(2)
        self.opponentScoreLcd.setSegmentStyle(QLCDNumber.Filled)

        layoyt = QGridLayout()
        self.scoreLabel = QLabel('Score: ')
        # tmp
        self.gameWidget = QGame(game.players.ai.EuristicsBot('Bot'))
        self.gameWidget.gameEnded.connect(self.updateScoreAndReset)
        self.exitButton = QPushButton('Exit to menu')
        layoyt.addWidget(QLabel('You'), 0, 0)
        layoyt.addWidget(QLabel('Opponent'), 0, 1)
        layoyt.addWidget(self.playerScoreLcd, 1, 0)
        layoyt.addWidget(self.opponentScoreLcd, 1, 1)
        layoyt.addWidget(self.gameWidget, 2, 0, 1, 2)
        layoyt.addWidget(self.exitButton, 3, 0)
        self.setLayout(layoyt)
        self.resize(400, 750)

    def updateScoreAndReset(self):
        print('usr')
        self.numberOfGames -= 1
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
        if self.numberOfGames > 0:
            self.gameWidget.reset(self.playerIsNotFirst)
        else:
            pass
