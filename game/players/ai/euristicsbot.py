from .. import Player
from .euristics import winning_move, not_losing_moves
import random


class EuristicsBot(Player):
    def choose_move(self, macroboard):
        if winning_move(macroboard) is not None:
            return winning_move(macroboard)
        not_losing = not_losing_moves(macroboard)
        if len(not_losing) > 1:
            return random.choice(not_losing)
        return random.choice(macroboard.available_moves)
