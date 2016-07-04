from .. import Player
from .heuristics import winning_move, not_losing_moves
from ...boards import GameEndedError
import random
from copy import deepcopy
import math
# from .minimax import minimax
from .alphabeta import alphaBeta


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
        print('calcmove')
        bestmove = None
        bestscore = - math.inf
        macroboard = deepcopy(macroboard)
        if not macroboard.available_moves:
            raise GameEndedError
        moves = macroboard.available_moves
        for px, py in moves:
            print('         checkmove')
            macroboard.make_move(px, py)
            # move_score = minimax(macroboard, 2, False)
            move_score = alphaBeta(macroboard, 2)
            if move_score > bestscore:
                bestscore = move_score
                bestmove = (px, py)
            macroboard.undo_last_move()
        return bestmove
