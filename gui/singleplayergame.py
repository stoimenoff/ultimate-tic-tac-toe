import game
from . import QGame
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel


class SinglePlayerGame(QWidget):
    def __init__(self, difficulty, numberOfGames):
        super(SinglePlayerGame, self).__init__()
        self.difficulty = difficulty
        self.numberOfGames = numberOfGames
        self.playerScore = 0
        self.opponentScore = 0
        self.playerIsNotFirst = False

        layoyt = QVBoxLayout()
        self.scoreLabel = QLabel('Score: ')
        # tmp
        self.gameWidget = QGame(game.players.ai.EuristicsBot('Bot'))
        self.gameWidget.gameEnded.connect(self.updateScoreAndReset)
        self.exitButton = QPushButton('Exit to menu')
        layoyt.addWidget(self.scoreLabel)
        layoyt.addWidget(self.gameWidget)
        layoyt.addWidget(self.exitButton)
        self.setLayout(layoyt)

    def updateScoreAndReset(self):
        print('usr')
        self.numberOfGames -= 1
        self.playerIsNotFirst = not self.playerIsNotFirst
        result = self.gameWidget.board.state
        if result == game.boards.State.X_WON:
            self.playerScore += 2
        elif result == game.boards.State.O_WON:
            self.opponentScore += 2
        self.playerScore += 1
        self.opponentScore += 1
        if self.numberOfGames > 0:
            self.gameWidget.reset(self.playerIsNotFirst)
        else:
            pass
