from copy import deepcopy
from ...boards import Square, State


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


@deepcopy_board
def number_of_winning_moves(macroboard):
    wins = 0
    moves = macroboard.available_moves
    for px, py in moves:
        macroboard.make_move(px, py)
        if macroboard.has_a_winner:
            wins += 1
        macroboard.undo_last_move()
    return wins


@deepcopy_board
def losing_moves(macroboard):
    moves = macroboard.available_moves
    losing = []
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


def boards_player_on_turn_won(macroboard):
    won = []
    on_turn = macroboard.get_on_turn()
    for i in range(macroboard.SIZE):
        for j in range(macroboard.SIZE):
            if macroboard.boards[i][j].winner == on_turn:
                won.append((i, j))
    return won


def player_to_state(player):
    if player == Square.X:
        return State.X_WON
    if player == Square.O:
        return State.O_WON
    raise ValueError('Invalid player')

CENTRAL = (1, 1)
CORNERS = [(0, 0), (0, 2), (2, 0), (2, 2)]

SCORE_FOR_WINNING_SQUARE = 10000
SCORE_FOR_WON_BOARD = 5
SCORE_FOR_WON_CENTRAL_BOARD = 10
SCORE_FOR_WON_CORNER_BOARD = 3

SCORE_FOR_TWO_SQUARES_IN_A_ROW = 2
SCORE_FOR_TWO_BOARDS_IN_A_ROW = 4

SCORE_FOR_SQUARE_IN_CENTRAL = 3
SCORE_FOR_CENTRAL_IN_BOARD = 3


def two_squares_in_a_row(microboard, on_turn):
    twos = 0
    for line in microboard.lines():
        if line.count(on_turn) == 2 and line.count(Square.EMPTY) == 1:
            twos += 1
    return twos


def two_boards_in_a_row(macroboard, on_turn):
    twos = 0
    state = player_to_state(on_turn)
    for line in macroboard.state_lines():
        if line.count(state) == 2 and line.count(State.IN_PROGRESS) == 1:
            twos += 1
    return twos


def squares_won(microboard, on_turn):
    return sum(map(lambda line: line.count(on_turn), microboard.export_grid()))


def score_microboard(microboard, i, j, on_turn):
    score = 0
    if microboard.winner == on_turn:
        score += SCORE_FOR_WON_BOARD
        if (i, j) == CENTRAL:
            score += SCORE_FOR_WON_CENTRAL_BOARD
        if (i, j) in CORNERS:
            score += SCORE_FOR_WON_CORNER_BOARD
        return score
    if microboard.state != State.IN_PROGRESS:
        return score
    if (i, j) == CENTRAL:
        score += squares_won(microboard, on_turn) * SCORE_FOR_SQUARE_IN_CENTRAL
    if microboard[CENTRAL[0]][CENTRAL[1]] == on_turn:
        score += SCORE_FOR_CENTRAL_IN_BOARD
    twos = two_squares_in_a_row(microboard, on_turn)
    score += twos * SCORE_FOR_TWO_SQUARES_IN_A_ROW
    return score


def score(macroboard):
    score = 0
    on_turn = macroboard.get_on_turn()
    for i in range(macroboard.SIZE):
        for j in range(macroboard.SIZE):
            score += score_microboard(macroboard[i][j], i, j, on_turn)
            winning_moves = number_of_winning_moves(macroboard)
            score += winning_moves * SCORE_FOR_WINNING_SQUARE
    twos = two_boards_in_a_row(macroboard, on_turn)
    score += twos * SCORE_FOR_TWO_BOARDS_IN_A_ROW
    return score
