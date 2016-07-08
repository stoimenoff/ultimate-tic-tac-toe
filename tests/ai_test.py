import unittest
from unittest.mock import patch, PropertyMock

from ultimatetictactoe.game.players.ai import *
from ultimatetictactoe.game.boards import Macroboard, GameEndedError, Square


class TestBots(unittest.TestCase):
    MOVES = [(2, 2), (7, 6), (3, 2), (1, 7), (3, 4), (2, 5),
             (7, 7), (4, 4), (4, 3), (4, 2), (3, 7), (0, 4), (2, 3),
             (8, 2), (6, 8), (1, 8), (5, 7), (6, 5), (2, 8), (8, 6),
             (6, 1), (0, 3), (0, 0), (2, 1), (8, 4), (6, 4), (1, 5),
             (4, 7), (3, 3), (2, 0), (8, 1), (6, 3), (0, 2), (2, 7),
             (8, 7), (6, 0), (1, 0), (5, 0), (6, 2), (0, 7), (2, 4),
             (8, 8), (6, 7), (1, 3), (5, 2), (8, 0), (7, 0), (3, 0),
             (1, 1), (5, 3), (7, 2), (3, 6), (5, 5), (7, 1), (3, 5)]

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

    def test_score_macroboard(self):
        board = Macroboard()
        scores_x = [2, 0, 0, 0, 0, 3, 3, 5, 5, 8, 8, 8, 8, 8, 8, 10, 10, 12,
                    12, 12, 10, 10, 10, 12, 12, 12, 12, 12, 10, 17, 17, 19, 19,
                    23, 25, 25, 25, 25, 25, 25, 25, 25, 25, 29, 29, 29, 29, 29,
                    29, 35, 33, 35, 37, 38, 34]
        scores_o = [0, 0, 0, 0, 2, 2, 2, 2, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9, 9,
                    11, 11, 15, 15, 15, 15, 17, 17, 19, 19, 19, 19, 22, 22, 24,
                    26, 26, 26, 26, 26, 28, 30, 28, 26, 26, 28, 28, 26, 28, 28,
                    33, 33, 35, 37, 45]
        for i in range(len(self.MOVES)):
            score_x = heuristics.score_macroboard(board, Square.X)
            score_o = heuristics.score_macroboard(board, Square.O)
            self.assertEqual(score_x, scores_x[i])
            self.assertEqual(score_o, scores_o[i])
            board.make_move(*self.MOVES[i])
        score_x = heuristics.score_macroboard(board, Square.X)
        score_o = heuristics.score_macroboard(board, Square.O)
        self.assertEqual(score_x, 10000)
        self.assertEqual(score_o, 33)

        board = Macroboard()
        for i in range(len(self.MOVES)):
            score = heuristics.score(board)
            expected = (scores_x[i] - scores_o[i]) * (-1)**i
            self.assertEqual(score, expected)
            board.make_move(*self.MOVES[i])
