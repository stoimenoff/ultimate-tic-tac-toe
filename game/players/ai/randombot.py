from .. import Player
import random


class RandomBot(Player):
    def choose_move(macroboard):
        return random.choice(macroboard.available_moves)
