from ...boards import State
from .heuristics import score
from copy import deepcopy
import math


def minimax(macroboard, depth):

    if macroboard.state != State.IN_PROGRESS or depth <= 0:
        return score(macroboard)
    bestscore = - math.inf
    moves = macroboard.available_moves
    for px, py in moves:
        child = deepcopy(macroboard)
        child.make_move(px, py)
        move_score = - minimax(child, depth - 1)
        if move_score > bestscore:
            bestscore = move_score
    return bestscore
