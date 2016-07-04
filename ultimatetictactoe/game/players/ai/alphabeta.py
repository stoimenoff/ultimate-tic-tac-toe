from ...boards import State
from .heuristics import score, SCORE_FOR_WIN
from copy import deepcopy


def reduce_depth(depth, number_of_moves):
    new_depth = depth
    if number_of_moves > 9:
        new_depth -= 1
    return new_depth


def alphaBeta(macroboard, depth):
    alpha = - SCORE_FOR_WIN
    beta = SCORE_FOR_WIN
    return alphaBetaMin(macroboard, alpha, beta, depth)


def alphaBetaMax(macroboard, alpha, beta, depth):
    if macroboard.state != State.IN_PROGRESS or depth <= 0:
        return score(macroboard)
    moves = macroboard.available_moves
    # depth = reduce_depth(depth, len(moves))
    best_score = - SCORE_FOR_WIN
    for px, py in moves:
        child = deepcopy(macroboard)
        child.make_move(px, py)
        best_score = max(alphaBetaMin(child, alpha, beta, depth - 1),
                         best_score)
        alpha = max(alpha, best_score)
        if beta <= alpha:
            break
    return best_score


def alphaBetaMin(macroboard, alpha, beta, depth):
    if macroboard.state != State.IN_PROGRESS or depth <= 0:
        return - score(macroboard)
    moves = macroboard.available_moves
    # depth = reduce_depth(depth, len(moves))
    best_score = SCORE_FOR_WIN
    for px, py in moves:
        child = deepcopy(macroboard)
        child.make_move(px, py)
        best_score = min(alphaBetaMax(child, alpha, beta, depth - 1),
                         best_score)
        beta = min(beta, best_score)
        if beta <= alpha:
            break
    return best_score
