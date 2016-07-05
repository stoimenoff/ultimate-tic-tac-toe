from .microboard import Microboard
from .boarditems import State, Square, IllegalMoveError, GameEndedError
from copy import deepcopy


class Macroboard:
    """
    Represents the big board of the game by a grid of Microboards.

    By default the board is full of empty microboards.

    Size of the board is passed to the constructor and can differ
    between 3 and 9. Invalid size raises a ValueError.
    Microboards are numbered by rows and columns, starting from 0.

    Keeps track of the moves made and the player who is on turn.
    By default the first player to play is Square.X.
    Optional parameter in the constructor can change that.

    *Note*
    Squares in the microboards are numbered by rows and columns,
    from 0 to size**2 The (row, column) of the square is its position.
    A square's coordinates is a tuple of four elements (x, y, i, j),
    where the (x, y) are the row and column of the microboard,
    the square is in, and (i, j) are the row and column of the square in
    that microboard.
    """
    def __init__(self, x_is_first=True, size=3):
        if size < 3 or size > 9:
            raise ValueError('Invalid board size!')
        self.SIZE = size
        self.boards = [[Microboard(size) for _ in range(size)]
                       for _ in range(size)]
        self.__on_turn = Square.X if x_is_first else Square.O
        self.last_move = None
        self.history = []

    @property
    def dead_boards(self):
        """
        Returns a list of (row, column) of the microboards
        that are not in progress.
        """
        return [(i, j) for i in range(self.SIZE) for j in range(self.SIZE)
                if self.boards[i][j].state != State.IN_PROGRESS]

    @property
    def active_boards(self):
        """
        Returns a list of (row, column) of the microboards
        that are in progress.
        """
        return [(i, j) for i in range(self.SIZE) for j in range(self.SIZE)
                if self.boards[i][j].state == State.IN_PROGRESS]

    def to_coords(self, px, py):
        """
        Converts a square position (px, py) to square coordinates (x, y, i, j).
        """
        if px not in range(self.SIZE**2) or py not in range(self.SIZE**2):
            raise IndexError
        return (px // self.SIZE, py // self.SIZE,
                px % self.SIZE, py % self.SIZE)

    def to_position(self, x, y, i, j):
        """
        Converts a square coordinates (x, y, i, j) to square position (px, py).
        """
        return (x * self.SIZE + i, y * self.SIZE + j)

    def coords_to_positions(self, coords):
        """
        Converts a list of coordinates to a list of positions.
        """
        return [self.to_position(x, y, i, j) for (x, y, i, j) in coords]

    def positions_to_coords(self, positions):
        """
        Converts a list of positions to a list of coordinates.
        """
        return [self.to_coords(px, py) for (px, py) in positions]

    def board_empty_positions(self, x, y):
        """
        Returns the positions of the empty squares in the (x, y) microboard.
        """
        board = self.boards[x][y]
        coords = [(x, y, i, j) for (i, j) in board.empty_squares]
        return self.coords_to_positions(coords)

    @property
    def available_boards(self):
        """
        A list of (row, column) of the boards that can currently be played.
        *Note* Depends on the last move that was made.
        Returns and empty list if the game has ended.
        """
        if self.state != State.IN_PROGRESS:
            return []
        if self.last_move is None:
            return self.active_boards
        x, y = self.last_move[-2:]
        if self.boards[x][y].state == State.IN_PROGRESS:
            return [(x, y)]
        return self.active_boards

    def can_play_on_all_active(self):
        """
        Returns True if a move is currently possible on all of the
        active microboards.
        Returns False otherwise.
        """
        if self.last_move is None:
            return True
        x, y = self.last_move[-2:]
        if self.boards[x][y].state != State.IN_PROGRESS:
            return True
        return False

    @property
    def available_moves(self):
        """
        A list of the positions of all possible moves.
        """
        moves = []
        for x, y in self.available_boards:
            moves.extend([self.to_position(x, y, i, j) for (i, j)
                         in self.boards[x][y].empty_squares])
        return moves

    @property
    def state(self):
        """
        The current state of the game.
        One of State.X_WON, State.O_WON, State.DRAW, State.IN_PROGRESS
        """
        lines = self.state_lines()
        for line in lines:
            if set(line) == {State.X_WON}:
                return State.X_WON
            if set(line) == {State.O_WON}:
                return State.O_WON
        if not any(map(lambda line: State.IN_PROGRESS in line, lines)):
            return State.DRAW
        return State.IN_PROGRESS

    @property
    def has_a_winner(self):
        """
        True, if a player has won the game,
        False otherwise.
        """
        return self.state in {State.X_WON, State.O_WON}

    def make_move(self, px, py):
        """
        Makes a move on the position (px, py).
        The player who is on turn is determined automatically.

        If the game has ended raises GameEndedError.
        If the move is not available raises IllegalMoveError.
        """
        if self.state != State.IN_PROGRESS:
            raise GameEndedError('Cannot make move. The game has ended.')
        x, y, i, j = self.to_coords(px, py)
        board = self.boards[x][y]
        if (x, y) not in self.available_boards:
            raise IllegalMoveError('Illegal move. Board is unavailable.')
        board.set_square(i, j, self.__on_turn)
        self.__on_turn = Square.X if self.__on_turn == Square.O else Square.O
        self.last_move = (x, y, i, j)
        self.history.append(self.last_move)

    def undo_last_move(self):
        """
        Undo the last move made.
        """
        if self.last_move is None:
            return
        x, y, i, j = self.last_move
        self.boards[x][y].undo_last_move()
        if len(self.history) > 1:
            self.last_move = self.history[-2]
        else:
            self.last_move = None
        self.__on_turn = Square.X if self.__on_turn == Square.O else Square.O
        del self.history[-1]

    def get_on_turn(self):
        """
        Return the player who is on turn.
        Either Square.X or Square.O
        """
        return deepcopy(self.__on_turn)

    def state_lines(self):
        lines = [[board.state for board in row] for row in self.boards]
        columns = [list(column) for column in zip(*lines)]
        diagonals = [[lines[i][i] for i in range(self.SIZE)],
                     [lines[i][self.SIZE - i - 1] for i in range(self.SIZE)]]
        lines.extend(columns)
        lines.extend(diagonals)
        return lines

    def winner(self):
        """
        Returns Square.X or Square.O if the corresponding player won the game.
        returns None otherwise.
        """
        state = self.state
        if state == State.X_WON:
            return Square.X
        if state == State.O_WON:
            return Square.O
        return None

    def __str__(self):
        """
        String representation of the macroboard for
        visualizing in the command line.
        """
        str = '-' * (self.SIZE ** 2 + self.SIZE + 1) + '\n'
        for row in self.boards:
            for i in range(self.SIZE):
                str += '|'
                for board in row:
                    for square in board.export_grid()[i]:
                        str += square.value
                    str += '|'
                str += '\n'
            str += '-' * (self.SIZE ** 2 + self.SIZE + 1) + '\n'
        return str

    def macro_str(self):
        """
        String representation of the microboards' results for
        visualizing in the command line.
        """
        str = '-' * (2 * self.SIZE + 1) + '\n'
        for row in self.boards:
            str += ' '
            for board in row:
                str += board.state.value + ' '
            str += '\n' + '-' * (2 * self.SIZE + 1) + '\n'
        return str
