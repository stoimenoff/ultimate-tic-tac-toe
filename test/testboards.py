import unittest
from copy import deepcopy

from game.boards import *


class TestMicroboard(unittest.TestCase):
    def setUp(self):
        self.board = Microboard()

    def test_size_exception(self):
        with self.assertRaises(ValueError):
            self.board = Microboard(10)
        with self.assertRaises(ValueError):
            self.board = Microboard(2)

    def test_x_win(self):
        self.board.set_square(0, 0, Square.X)
        self.board.set_square(0, 1, Square.X)
        self.board.set_square(0, 2, Square.X)
        self.assertEqual(self.board.state, State.X_WON)

    def test_o_win(self):
        self.board.set_square(0, 0, Square.O)
        self.board.set_square(1, 1, Square.O)
        self.board.set_square(2, 2, Square.O)
        self.assertEqual(self.board.state, State.O_WON)

    def test_draw(self):
        self.board.set_square(0, 0, Square.O)
        self.board.set_square(0, 1, Square.O)
        self.board.set_square(0, 2, Square.X)
        self.board.set_square(1, 0, Square.X)
        self.board.set_square(1, 1, Square.X)
        self.board.set_square(1, 2, Square.O)
        self.board.set_square(2, 0, Square.O)
        self.board.set_square(2, 1, Square.X)
        self.board.set_square(2, 2, Square.X)
        self.assertEqual(self.board.state, State.DRAW)

    def test_set_square(self):
        self.board.set_square(0, 0, Square.X)
        self.assertEqual(self.board.export_grid()[0][0], Square.X)
        with self.assertRaises(IllegalMoveError):
            self.board.set_square(0, 0, Square.O)
        with self.assertRaises(IllegalMoveError):
            self.board.set_square(0, 0, Square.EMPTY)

    def test_history(self):
        history = [(0, 0), (0, 1), (2, 1)]
        self.board.set_square(0, 0, Square.X)
        self.board.set_square(0, 1, Square.X)
        self.board.set_square(2, 1, Square.X)
        self.assertEqual(self.board.history, history)
        del history[-1]
        self.board.undo_last_move()
        self.assertEqual(self.board.history, history)

    def test_empty_squares(self):
        self.board.set_square(0, 0, Square.O)
        self.board.set_square(0, 1, Square.O)
        self.board.set_square(0, 2, Square.X)
        self.board.set_square(2, 1, Square.O)
        self.board.set_square(2, 2, Square.O)
        expected = {(1, 0), (1, 1), (1, 2), (2, 0)}
        self.assertEqual(set(self.board.empty_squares), expected)

    def test_undo_last_move(self):
        grid = deepcopy(self.board.grid)
        move = deepcopy(self.board.last_move)
        self.board.set_square(0, 0, Square.X)
        self.board.undo_last_move()
        self.assertEqual(grid, self.board.grid)
        self.assertEqual(move, self.board.last_move)


class TestMacroboard(unittest.TestCase):
    MOVES = [(2, 2), (7, 6), (3, 2), (1, 7), (3, 4), (2, 5),
             (7, 7), (4, 4), (4, 3), (4, 2), (3, 7), (0, 4), (2, 3),
             (8, 2), (6, 8), (1, 8), (5, 7), (6, 5), (2, 8), (8, 6),
             (6, 1), (0, 3), (0, 0), (2, 1), (8, 4), (6, 4), (1, 5),
             (4, 7), (3, 3), (2, 0), (8, 1), (6, 3), (0, 2), (2, 7),
             (8, 7), (6, 0), (1, 0), (5, 0), (6, 2), (0, 7), (2, 4),
             (8, 8), (6, 7), (1, 3), (5, 2), (8, 0), (7, 0), (3, 0),
             (1, 1), (5, 3), (7, 2), (3, 6), (5, 5), (7, 1), (3, 5)]

    def setUp(self):
        self.board = Macroboard()

    def play_board(self):
        self.board = Macroboard()
        for move in self.MOVES:
            self.board.make_move(*move)

    def test_make_move(self):
        self.board.make_move(0, 0)
        square = self.board.boards[0][0].grid[0][0]
        self.assertEqual(square, Square.X)

        self.board.make_move(0, 2)
        square = self.board.boards[0][0].grid[0][2]
        self.assertEqual(square, Square.O)

        with self.assertRaises(IllegalMoveError):
            self.board.make_move(0, 0)
        with self.assertRaises(IllegalMoveError):
            self.board.make_move(4, 4)

        self.play_board()
        with self.assertRaises(GameEndedError):
            self.board.make_move(4, 4)
        with self.assertRaises(GameEndedError):
            self.board.make_move(0, 2)

    def test_history(self):
        HISTORY = [self.board.to_coords(*move) for move in self.MOVES]
        for i in range(len(self.MOVES)):
            self.board.make_move(*self.MOVES[i])
            self.assertEqual(HISTORY[:i + 1], self.board.history)
            self.assertEqual(HISTORY[i], self.board.last_move)
        for i in range(len(self.MOVES) - 1, 0, -1):
            self.board.undo_last_move()
            self.assertEqual(HISTORY[:i], self.board.history)
            self.assertEqual(HISTORY[i - 1], self.board.last_move)
        self.board.undo_last_move()
        self.assertEqual([], self.board.history)
        self.assertEqual(None, self.board.last_move)
        self.board.undo_last_move()
        self.assertEqual([], self.board.history)
        self.assertEqual(None, self.board.last_move)

    def test_to_coords(self):
        self.assertEqual(self.board.to_coords(0, 0), (0, 0, 0, 0))
        self.assertEqual(self.board.to_coords(0, 1), (0, 0, 0, 1))
        self.assertEqual(self.board.to_coords(0, 2), (0, 0, 0, 2))
        self.assertEqual(self.board.to_coords(1, 3), (0, 1, 1, 0))
        self.assertEqual(self.board.to_coords(4, 4), (1, 1, 1, 1))
        self.assertEqual(self.board.to_coords(5, 7), (1, 2, 2, 1))
        self.assertEqual(self.board.to_coords(2, 3), (0, 1, 2, 0))
        self.assertEqual(self.board.to_coords(2, 4), (0, 1, 2, 1))
        self.assertEqual(self.board.to_coords(0, 8), (0, 2, 0, 2))
        self.assertEqual(self.board.to_coords(8, 0), (2, 0, 2, 0))
        self.assertEqual(self.board.to_coords(8, 8), (2, 2, 2, 2))

    def test_to_positions(self):
        POSITIONS = [(0, 0), (0, 1), (0, 2), (1, 3), (4, 4), (5, 7), (2, 3),
                     (2, 4), (0, 8), (8, 0), (8, 8)]
        for position in POSITIONS:
            coords = self.board.to_coords(*position)
            self.assertEqual(self.board.to_position(*coords), position)

    def test_size_exception(self):
        with self.assertRaises(ValueError):
            self.board = Macroboard(True, 10)
        with self.assertRaises(ValueError):
            self.board = Macroboard(True, 2)

    def test_dead_boards(self):
        dead = self.board.dead_boards
        self.assertFalse(dead)
        self.play_board()
        self.board.undo_last_move()
        dead = [(0, 0), (0, 2), (2, 0), (2, 1), (2, 2)]
        self.assertEqual(self.board.dead_boards, dead)


if __name__ == '__main__':
    unittest.main()
