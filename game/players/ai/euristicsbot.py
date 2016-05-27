from .. import Player
from .euristics import winning_move
import random


class EuristicsBot(Player):
    def choose_move(self, macroboard):
        if winning_move(macroboard) is not None:
            return winning_move(macroboard)
        return random.choice(macroboard.available_moves)
