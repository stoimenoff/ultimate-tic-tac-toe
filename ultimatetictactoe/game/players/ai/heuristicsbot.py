from .. import Player
from .heuristics import winning_move, not_losing_moves, score
from ...boards import GameEndedError, Square
import random
from copy import deepcopy
import math


class EuristicsBot(Player):
    def choose_move(self, macroboard):
        if not macroboard.available_moves:
            raise GameEndedError
        if winning_move(macroboard) is not None:
            return winning_move(macroboard)
        not_losing = not_losing_moves(macroboard)
        if len(not_losing) > 1:
            return random.choice(not_losing)
        return random.choice(macroboard.available_moves)


class HeuristicsBot(Player):
    def choose_move(self, macroboard):
        me = macroboard.get_on_turn()
        opponent = Square.X if me == Square.O else Square.O
        bestmove = None
        bestscore = - math.inf
        macroboard = deepcopy(macroboard)
        if not macroboard.available_moves:
            raise GameEndedError
        moves = macroboard.available_moves
        for px, py in moves:
            macroboard.make_move(px, py)
            my_score = score(macroboard, me)
            opponent_score = score(macroboard, opponent)
            if my_score - opponent_score > bestscore:
                bestscore = my_score - opponent_score
                bestmove = (px, py)
            macroboard.undo_last_move()
        return bestmove
