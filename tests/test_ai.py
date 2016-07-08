import unittest
from unittest.mock import patch, PropertyMock

from ultimatetictactoe.game.players.ai import *
from ultimatetictactoe.game.boards import Macroboard, GameEndedError


class TestBots(unittest.TestCase):
    def test_selector(self):
        self.assertIsInstance(select_bot(1), GentlemanBot)
        self.assertIsInstance(select_bot(2), RandomBot)
        self.assertIsInstance(select_bot(3), HeuristicsBot)
        self.assertIsInstance(select_bot(4), AlphaBetaBot)
        for i in range(5, 10):
            with self.assertRaises(ValueError):
                select_bot(i)
        for i in range(0, -6, -1):
            with self.assertRaises(ValueError):
                select_bot(i)

    def test_choose_move(self):
        board = Macroboard()
        for difficulty in range(1, 5):
            bot = select_bot(difficulty)
            move = bot.choose_move(board)
            self.assertIn(move, board.available_moves)
        with patch('ultimatetictactoe.game.boards.Macroboard.available_moves',
                   new_callable=PropertyMock) as mock_moves:
            mock_moves.return_value = []
            for difficulty in range(1, 5):
                bot = select_bot(difficulty)
                with self.assertRaises(GameEndedError):
                    bot.choose_move(board)
