from .. import Player
from ...boards import GameEndedError
import random


class RandomBot(Player):
    def choose_move(self, macroboard):
        if not macroboard.available_moves:
            raise GameEndedError
        return random.choice(macroboard.available_moves)
