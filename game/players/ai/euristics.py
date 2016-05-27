from copy import deepcopy


def deepcopy_board(function):
    def with_copied_board(macroboard, *args):
        return function(deepcopy(macroboard), *args)
    return with_copied_board


@deepcopy_board
def winning_move(macroboard):
    moves = macroboard.available_moves
    for px, py in moves:
        macroboard.make_move(px, py)
        if macroboard.has_a_winner:
            return (px, py)
        macroboard.undo_last_move()
    return None
