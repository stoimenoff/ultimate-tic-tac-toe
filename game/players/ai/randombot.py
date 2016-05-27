from .. import Player
import random


class RandomBot(Player):
    def choose_move(self, macroboard):
        return random.choice(macroboard.available_moves)
