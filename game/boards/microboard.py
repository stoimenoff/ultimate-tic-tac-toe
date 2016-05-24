from copy import deepcopy
from .boarditems import State, Square, IllegalMoveError


class Microboard:
    def __init__(self, size=3):
        if size < 3 or size > 9:
            raise ValueError('Invalid board size!')
        self.SIZE = size
        self.__grid = [[Square.EMPTY] * size for _ in range(size)]

    @property
    def state(self):
        lines = deepcopy(self.__grid)
        columns = zip(*self.__grid)
        lines.extend(columns)
        diagonals = [[self.__grid[i][i] for i in range(self.SIZE)],
                     [self.__grid[i][self.SIZE - i - 1] for i in
                     range(self.SIZE)]]
        lines.extend(diagonals)

        for line in lines:
            if set(line) == {Square.X}:
                return State.X_WON
            if set(line) == {Square.O}:
                return State.O_WON
        if not any(map(lambda line: Square.EMPTY in line, self.__grid)):
            return State.DRAW
        return State.IN_PROGRESS

    def set_square(self, x, y, value):
        if self.state != State.IN_PROGRESS:
            raise IllegalMoveError('Board is dead!')
        if self.__grid[x][y] != Square.EMPTY:
            raise IllegalMoveError('Square is already played!')
        if value not in {Square.X, Square.O}:
            raise IllegalMoveError('Move value is incorrect!')
        self.__grid[x][y] = value

    @property
    def empty_squares(self):
        return [(i, j) for i in range(self.SIZE) for j in range(self.SIZE)
                if self.__grid[i][j] == Square.EMPTY]

    def export_grid(self):
        return deepcopy(self.__grid)
