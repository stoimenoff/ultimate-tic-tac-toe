from enum import Enum


class State(Enum):
    """
    Represents a board state.
    """
    X_WON = 'X'
    O_WON = 'O'
    DRAW = '-'
    IN_PROGRESS = ' '


class Square(Enum):
    """
    Represents a board square.
    """
    EMPTY = ' '
    X = 'X'
    O = 'O'


class IllegalMoveError(Exception):
    pass


class GameEndedError(Exception):
    pass
