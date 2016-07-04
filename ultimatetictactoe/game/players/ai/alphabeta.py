from ...boards import State
from .heuristics import score, SCORE_FOR_WIN
from copy import deepcopy


DEPTH_BALANCE = {(1, 2): 2,
                 (2, 4): 1,
                 (4, 5): 0,
                 (5, 10): 0,
                 (10, 20): -1,
                 (20, 30): -1,
                 (30, 40): -2,
                 (40, 50): -2,
                 (50, 60): -2,
                 (60, 70): -2,
                 (70, 82): -2}


def balance_depth(depth, number_of_moves):
    new_depth = depth
    for (low, high), balance in DEPTH_BALANCE.items():
        if low <= number_of_moves < high:
            new_depth += balance
    return new_depth


def alphaBeta(macroboard, depth):
    alpha = - SCORE_FOR_WIN
    beta = SCORE_FOR_WIN
    return alphaBetaMin(macroboard, alpha, beta, depth)


def alphaBetaMax(macroboard, alpha, beta, depth):
    if macroboard.state != State.IN_PROGRESS or depth <= 0:
        return score(macroboard)
    best_score = - SCORE_FOR_WIN
    moves = macroboard.available_moves
    depth = balance_depth(depth, len(moves))
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
    depth = balance_depth(depth, len(moves))
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
