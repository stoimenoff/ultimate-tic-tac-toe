from copy import deepcopy


def deepcopy_board(function):
    def with_copied_board(macroboard, *args):
        return function(deepcopy(macroboard), *args)
    return with_copied_board


@deepcopy_board
def winning_move(macroboard):
    moves = macroboard.available_moves
    # print('calc winning move? Possible moves: ', len(moves))
    for px, py in moves:
        macroboard.make_move(px, py)
        if macroboard.has_a_winner:
            return (px, py)
        macroboard.undo_last_move()
    return None


@deepcopy_board
def losing_moves(macroboard):
    moves = macroboard.available_moves
    losing = []
    # print('calc losing moves. Possible moves: ', len(moves))
    for px, py in moves:
        macroboard.make_move(px, py)
        if winning_move(macroboard) is not None:
            losing.append((px, py))
        macroboard.undo_last_move()
    return losing


def not_losing_moves(macroboard):
    moves = macroboard.available_moves
    losing = losing_moves(macroboard)
    return [move for move in moves if move not in losing]
