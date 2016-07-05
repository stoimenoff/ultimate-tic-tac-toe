from copy import deepcopy
from .boarditems import State, Square, IllegalMoveError


class Microboard:
    """
    Represents one of the small boards in the game.

    By default the board is full of empty squares.

    Size of the board is passed to the constructor and can differ
    between 3 and 9. Invalid size raises a ValueError.
    Board squares are numbered by rows and columns, starting from 0.
    Square value is changed via 'set_square'.

    Keeps track of the moves made.
    """
    def __init__(self, size=3):
        if size < 3 or size > 9:
            raise ValueError('Invalid board size!')
        self.SIZE = size
        self.grid = [[Square.EMPTY] * size for _ in range(size)]
        self.last_move = None
        self.history = []

    @property
    def state(self):
        """
        The current state of the board.
        One of State.X_WON, State.O_WON, State.DRAW, State.IN_PROGRESS
        """
        lines = self.lines()
        for line in lines:
            if set(line) == {Square.X}:
                return State.X_WON
            if set(line) == {Square.O}:
                return State.O_WON
        if not any(map(lambda line: Square.EMPTY in line, self.grid)):
            return State.DRAW
        return State.IN_PROGRESS

    def set_square(self, x, y, value):
        """
        x and y represent the square's row and column.

        value should be one of Square.X or Square.O
        ValueError is raised otherwise

        If the board is not in play or the square at (x, y)
        is not Empty IllegalMoveError is raised.
        """
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
        """
        Undo the last move made on the board.
        """
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
        """
        A list of tuples (row, column) of the squares that are currently empty.
        """
        return [(i, j) for i in range(self.SIZE) for j in range(self.SIZE)
                if self.grid[i][j] == Square.EMPTY]

    def export_grid(self):
        """
        Deepcopy of the board's grid.
        """
        return deepcopy(self.grid)

    def winner(self):
        """
        Returns Square.X or Square.O if the corresponding player won the board.
        returns None otherwise.
        """
        state = self.state
        if state == State.X_WON:
            return Square.X
        if state == State.O_WON:
            return Square.O
        return None

    def lines(self):
        lines = deepcopy(self.grid)
        columns = [list(column) for column in zip(*lines)]
        diagonals = [[lines[i][i] for i in range(self.SIZE)],
                     [lines[i][self.SIZE - i - 1] for i in
                     range(self.SIZE)]]
        lines.extend(columns)
        lines.extend(diagonals)
        return lines
