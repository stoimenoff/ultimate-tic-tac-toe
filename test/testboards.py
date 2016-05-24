import unittest

from game.boards import *


class TestMicroboard(unittest.TestCase):
    def setUp(self):
        self.board = Microboard()

    def test_set_square(self):
        self.board.set_square(0, 0, Square.X)
        self.assertEqual(self.board.export_grid()[0][0], Square.X)
        with self.assertRaises(IllegalMoveError):
            self.board.set_square(0, 0, Square.O)
        with self.assertRaises(IllegalMoveError):
            self.board.set_square(0, 0, Square.EMPTY)


class TestMacroboard(unittest.TestCase):
    def setUp(self):
        self.board = Macroboard()

if __name__ == '__main__':
    unittest.main()
