from ...boards import State
from .heuristics import score
from .alphabeta import balance_depth
from copy import deepcopy
import math


def minimax(macroboard, depth, maximizing=True):
    """
    Perform a minimax search on a game moves tree.
    If optional parameter maximizing is True, assume that maximizing player
    is on turn. If is False - assume minimizing player. True, by default.
    """
    if macroboard.state != State.IN_PROGRESS or depth <= 0:
        return score(macroboard) * (maximizing * 2 - 1)

    if maximizing:
        bestscore = - math.inf
    else:
        bestscore = math.inf

    moves = macroboard.available_moves
    depth = balance_depth(depth, len(moves))
    for px, py in moves:
        child = deepcopy(macroboard)
        child.make_move(px, py)
        move_score = minimax(child, depth - 1, not maximizing)
        if maximizing:
            bestscore = max(bestscore, move_score)
        else:
            bestscore = min(bestscore, move_score)
    return bestscore
