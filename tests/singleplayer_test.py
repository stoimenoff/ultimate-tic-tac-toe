import PyQt5
from PyQt5.QtWidgets import QApplication
import sys
import unittest
import pickle
import tempfile
from unittest.mock import patch


from ultimatetictactoe.gui.singleplayer import *
from ultimatetictactoe.game.boards import Macroboard
from ultimatetictactoe.game.players.ai import select_bot

app = QApplication(sys.argv)


class TestSingleplyaerMenu(unittest.TestCase):

    def setUp(self):
        self.menu = SinglePlayerMenu()

    def tearDown(self):
        del self.menu

    def getButton(self, n):
        return self.menu.difficultyMenu.layout().itemAt(n - 1).widget()

    def testDifficultyChange(self):
        CLICKS = [1, 2, 4, 3, 4, 3, 2, 3, 4, 3, 2, 1]
        for button in CLICKS:
            self.getButton(button).click()
            self.assertEqual(self.menu.difficultySelected, button)

    def testCreateRadio(self):
        radio = self.menu.createRadio('text', 123)
        self.assertIsInstance(radio, PyQt5.QtWidgets.QRadioButton)
        self.assertEqual(radio.id, 123)
        self.assertEqual(radio.text(), 'text')

    def testCreateDifficultyMenu(self):
        box = self.menu.createDifficultyMenu()
        self.assertIsInstance(box, PyQt5.QtWidgets.QGroupBox)
        for i in range(3):
            try:
                radio = box.layout().itemAt(i).widget()
                self.assertIsInstance(radio, PyQt5.QtWidgets.QRadioButton)
                self.assertEqual(radio.id, i + 1)
            except Exception:
                self.fail('Radio error')
        fake = box.layout().itemAt(4).widget()
        self.assertFalse(fake)


class TestSinglePlayer(unittest.TestCase):
    def setUp(self):
        self.game = SinglePlayer()

    def tearDown(self):
        del self.game

    def testStartGame(self):
        self.assertIsNone(self.game.game)
        self.game.gameMenu.startButton.click()
        self.assertIsNotNone(self.game.game)
        self.assertIsInstance(self.game.game, SinglePlayerGame)
        self.assertEqual(self.game.game.difficulty,
                         self.game.gameMenu.difficultySelected)
        self.assertEqual(self.game.game.numberOfGames,
                         self.game.gameMenu.numberOfGamesSpinBox.value())
        self.assertEqual(self.game.stack.currentWidget(), self.game.game)

    @patch('PyQt5.QtWidgets.QFileDialog.getOpenFileName')
    def testLoadGame(self, openfile):
        board = Macroboard()
        config = (3, 4, 1, 3, 0, True, board)
        file = tempfile.NamedTemporaryFile()
        with open(file.name, 'wb') as f:
            pickle.dump(config, f)
        openfile.return_value = (file.name, '')
        self.game.loadGame()
        self.assertEqual(self.game.game.difficulty, 3)
        self.assertEqual(self.game.game.numberOfGames, 4)
        self.assertEqual(self.game.game.gamesPlayed, 1)
        self.assertEqual(self.game.game.playerScore, 3)
        self.assertEqual(self.game.game.opponentScore, 0)
        self.assertEqual(self.game.game.playerIsNotFirst, True)

    @patch('PyQt5.QtWidgets.QFileDialog.getOpenFileName')
    def testLoadInvalidGame(self, openfile):
        file = tempfile.NamedTemporaryFile()
        with open(file.name, 'wb') as f:
            pickle.dump('some fake stuff', f)
        openfile.return_value = (file.name, '')
        self.game.loadGame()
        self.assertEqual(self.game.game.difficulty, 1)
        self.assertEqual(self.game.game.numberOfGames, 1)
        self.assertEqual(self.game.game.gamesPlayed, 0)
        self.assertEqual(self.game.game.playerScore, 0)
        self.assertEqual(self.game.game.opponentScore, 0)
        self.assertEqual(self.game.game.playerIsNotFirst, False)


class TestSinglePlayerGame(unittest.TestCase):
    def setUp(self):
        self.game = SinglePlayerGame()

    def tearDown(self):
        del self.game

    @patch('PyQt5.QtWidgets.QLabel.show')
    def testDisplayMessage(self, show):
        MESSAGES = ['asd', 'asd2', 'asd3']
        for message in MESSAGES:
            self.game.displayMessage(message)
            self.assertEqual(self.game.message.text(), message)
            show.assert_any_call()

    def testCreateLabel(self):
        label = self.game.createLabel('test')
        self.assertIsInstance(label, PyQt5.QtWidgets.QLabel)
        self.assertEqual(label.text(), 'test')

    @patch('PyQt5.QtWidgets.QFileDialog.getSaveFileName')
    def testSaveGame(self, getSave):
        file = tempfile.NamedTemporaryFile()
        getSave.return_value = (file.name, '')
        self.game.saveGame()
        with file:
            config = pickle.load(file)
        self.assertTupleEqual(config[:5], self.game.getConfiguration()[:5])

    def testGetConfiguration(self):
        config = self.game.getConfiguration()
        self.assertIsInstance(self.game.difficulty, int)
        self.assertEqual(config[0], self.game.difficulty)
        self.assertIsInstance(self.game.numberOfGames, int)
        self.assertEqual(config[1], self.game.numberOfGames)
        self.assertIsInstance(self.game.gamesPlayed, int)
        self.assertEqual(config[2], self.game.gamesPlayed)
        self.assertIsInstance(self.game.playerScore, int)
        self.assertEqual(config[3], self.game.playerScore)
        self.assertIsInstance(self.game.opponentScore, int)
        self.assertEqual(config[4], self.game.opponentScore)
        self.assertIsInstance(self.game.playerIsNotFirst, bool)
        self.assertEqual(config[5], self.game.playerIsNotFirst)
        self.assertIsInstance(self.game.gameWidget.board, Macroboard)
        self.assertEqual(config[6], self.game.gameWidget.board)

    def testLoadConfiguration(self):
        board = Macroboard()
        config = (3, 4, 1, 3, 0, True, board)
        self.game.loadConfiguration(config)
        self.assertEqual(config, self.game.getConfiguration())

    def testUpdateScoreAndReset(self):
        games = self.game.gamesPlayed
        player = self.game.playerIsNotFirst
        score1 = self.game.playerScore
        score2 = self.game.opponentScore
        self.game.updateScoreAndReset()
        self.assertNotEqual(games, self.game.gamesPlayed)
        self.assertNotEqual(player, self.game.playerIsNotFirst)
        self.assertEqual(score1, self.game.playerScore)
        self.assertEqual(score2, self.game.opponentScore)


class TestBotGame(unittest.TestCase):
    def setUp(self):
        self.bot = select_bot(1)
        self.game = BotGame(self.bot)

    def tearDown(self):
        del self.game

    def getButton(self, x, y):
        microboard = self.game.qBoard.grid.itemAt(x).widget()
        return microboard.layout().itemAt(y).widget()

    @patch('ultimatetictactoe.game.boards.Macroboard.make_move')
    @patch('ultimatetictactoe.gui.QMacroBoard.setClickEnabled')
    def testClicks(self, enabled, make_move):
        self.getButton(0, 0).click()
        enabled.assert_called_with(False)
        make_move.assert_called_with(0, 0)

    def testLoadBoard(self):
        board = Macroboard()
        self.game.loadBoard(board)
        self.assertEqual(self.game.board, board)
