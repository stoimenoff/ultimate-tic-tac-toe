from .. import Player
from ...boards import GameEndedError
from copy import deepcopy
import math
from .alphabeta import alphaBeta, balance_depth
import random

DEPTH = 2


class GentlemanBot(Player):
    def choose_move(self, macroboard):
        worstmoves = []
        macroboard = deepcopy(macroboard)
        moves = macroboard.available_moves
        if not moves:
            raise GameEndedError
        worstscore = math.inf
        depth = balance_depth(DEPTH, len(moves))
        for px, py in moves:
            macroboard.make_move(px, py)
            move_score = alphaBeta(macroboard, depth)
            if move_score < worstscore:
                worstscore = move_score
                worstmoves = [(px, py)]
            if move_score == worstscore:
                worstmoves.append((px, py))
            macroboard.undo_last_move()
        return random.choice(worstmoves)
