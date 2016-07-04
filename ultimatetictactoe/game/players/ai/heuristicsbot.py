from .. import Player
from .heuristics import winning_move, not_losing_moves
from ...boards import GameEndedError
import random
from copy import deepcopy
import math
# from .minimax import minimax
from .alphabeta import alphaBeta, balance_depth
import datetime


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


DEPTH = 2


class HeuristicsBot(Player):
    def choose_move(self, macroboard):
        print('calcmove')
        bestmoves = []
        bestscore = - math.inf
        macroboard = deepcopy(macroboard)
        if not macroboard.available_moves:
            raise GameEndedError
        moves = macroboard.available_moves
        depth = balance_depth(DEPTH, len(moves))
        for px, py in moves:
            # print('         checkmove')
            macroboard.make_move(px, py)

            # t1 = datetime.datetime.now()
            # move_score = minimax(macroboard, depth, False)
            move_score = alphaBeta(macroboard, depth)
            '''
            delta = datetime.datetime.now() - t1
            print('         ', delta.total_seconds())
            if (delta.total_seconds() > 1):
                print(macroboard)
                print(depth)
            print('         checked')
            '''
            if move_score > bestscore:
                bestscore = move_score
                bestmoves = [(px, py)]
            if move_score == bestscore:
                bestmoves.append((px, py))
            macroboard.undo_last_move()
        return random.choice(bestmoves)
