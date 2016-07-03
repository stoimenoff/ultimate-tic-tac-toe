import sys
from gui import *
from gui.multiplayerclient import ClientGame
from gui.botbattle import BotBattle
from gui.spectatebotbattle import BotBattleMenu, SpectateBattle
from PyQt5.QtWidgets import QApplication
import game
# import pickle


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # window = SinglePlayerGame(1, 1)
    # window = SinglePlayer()
    # window = HotSeatGame()
    # window = ClientGame()
    # window = BotBattle(game.players.ai.EuristicsBot('B1'),
                       # game.players.ai.EuristicsBot('B2'))
    window = SpectateBattle()
    window.move(50, 50)
    window.show()
    sys.exit(app.exec_())
