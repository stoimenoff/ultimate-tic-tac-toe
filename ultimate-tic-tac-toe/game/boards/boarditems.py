from enum import Enum


class State(Enum):
    X_WON = 'X'
    O_WON = 'O'
    DRAW = '-'
    IN_PROGRESS = ' '


class Square(Enum):
    EMPTY = ' '
    X = 'X'
    O = 'O'


class IllegalMoveError(Exception):
    pass


class GameEndedError(Exception):
    pass
