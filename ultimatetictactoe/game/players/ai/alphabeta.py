from ...boards import State
from .heuristics import score, SCORE_FOR_WIN
from copy import deepcopy


def alphaBeta(macroboard, depth):
    alpha = - SCORE_FOR_WIN
    beta = SCORE_FOR_WIN
    return alphaBetaMax(macroboard, alpha, beta, depth)


def alphaBetaMax(macroboard, alpha, beta, depth):
    if macroboard.state != State.IN_PROGRESS or depth <= 0:
        return score(macroboard)
    moves = macroboard.available_moves
    for px, py in moves:
        child = deepcopy(macroboard)
        child.make_move(px, py)
        move_score = alphaBetaMin(child, alpha, beta, depth - 1)
        if move_score >= beta:
            return beta
        if move_score > alpha:
            alpha = move_score
    return alpha


def alphaBetaMin(macroboard, alpha, beta, depth):
    if macroboard.state != State.IN_PROGRESS or depth <= 0:
        return score(macroboard)
    moves = macroboard.available_moves
    for px, py in moves:
        child = deepcopy(macroboard)
        child.make_move(px, py)
        move_score = alphaBetaMax(child, alpha, beta, depth - 1)
        if move_score <= alpha:
            return alpha
        if move_score < beta:
            beta = move_score
    return beta
