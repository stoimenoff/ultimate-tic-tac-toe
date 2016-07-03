from copy import deepcopy
from .boarditems import State, Square, IllegalMoveError


class Microboard:
    def __init__(self, size=3):
        if size < 3 or size > 9:
            raise ValueError('Invalid board size!')
        self.SIZE = size
        self.grid = [[Square.EMPTY] * size for _ in range(size)]
        self.last_move = None
        self.history = []

    @property
    def state(self):
        lines = deepcopy(self.grid)
        columns = zip(*self.grid)
        lines.extend(columns)
        diagonals = [[self.grid[i][i] for i in range(self.SIZE)],
                     [self.grid[i][self.SIZE - i - 1] for i in
                     range(self.SIZE)]]
        lines.extend(diagonals)

        for line in lines:
            if set(line) == {Square.X}:
                return State.X_WON
            if set(line) == {Square.O}:
                return State.O_WON
        if not any(map(lambda line: Square.EMPTY in line, self.grid)):
            return State.DRAW
        return State.IN_PROGRESS

    def set_square(self, x, y, value):
        if self.state != State.IN_PROGRESS:
            raise IllegalMoveError('Board is dead!')
        if self.grid[x][y] != Square.EMPTY:
            raise IllegalMoveError('Square is already played!')
        if value not in {Square.X, Square.O}:
            raise IllegalMoveError('Move value is incorrect!')
        self.grid[x][y] = value
        self.last_move = (x, y)
        self.history.append(self.last_move)

    def undo_last_move(self):
        if self.last_move is None:
            return
        x, y = self.last_move
        self.grid[x][y] = Square.EMPTY
        if len(self.history) > 1:
            self.last_move = self.history[-2]
        else:
            self.last_move = None
        del self.history[-1]

    @property
    def empty_squares(self):
        return [(i, j) for i in range(self.SIZE) for j in range(self.SIZE)
                if self.grid[i][j] == Square.EMPTY]

    def export_grid(self):
        return deepcopy(self.grid)
