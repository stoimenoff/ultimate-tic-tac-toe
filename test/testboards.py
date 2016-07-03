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
    def setUp(self):
        self.board = Macroboard()

    def get_played_board(self):
        pass

    def get_dead_board(self):
        pass

    def test_make_move(self):
        self.board.make_move(0, 0)

    def test_history(self):
        pass

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
        '''
        for i in range(self.board.SIZE):
            for j in range(self.board.SIZE):
                self.assertIn((i, j), dead)
        '''

if __name__ == '__main__':
    unittest.main()
