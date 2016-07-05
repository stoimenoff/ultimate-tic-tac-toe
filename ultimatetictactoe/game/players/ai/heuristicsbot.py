from ...boards import GameEndedError
from .. import Player
from .heuristics import score  # , greedy_score
import random
from copy import deepcopy
import math


class HeuristicsBot(Player):
    """
    Bot player. Calculates his move only based on the heuristics' scores
    for the possible moves.
    """
    def choose_move(self, macroboard):
        bestmoves = []
        bestscore = - math.inf
        macroboard = deepcopy(macroboard)
        if not macroboard.available_moves:
            raise GameEndedError
        moves = macroboard.available_moves
        for px, py in moves:
            macroboard.make_move(px, py)
            move_score = - score(macroboard)
            # move_score = - greedy_score(macroboard)
            if move_score > bestscore:
                bestscore = move_score
                bestmoves = [(px, py)]
            if move_score == bestscore:
                bestmoves.append((px, py))
            macroboard.undo_last_move()
        return random.choice(bestmoves)
