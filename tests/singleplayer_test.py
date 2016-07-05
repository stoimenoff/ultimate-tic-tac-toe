import PyQt5
from PyQt5.QtWidgets import QApplication
import sys
import unittest
import pickle
import tempfile
from unittest.mock import patch


from ultimatetictactoe.gui.singleplayer import *
from ultimatetictactoe.game.boards import Macroboard

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


def tmpConfig():
    board = Macroboard()
    config = (3, 4, 1, 3, 0, True, board)
    file = tempfile.NamedTemporaryFile()
    with open(file.name, 'wb') as f:
        pickle.dump(config, f)
    return (file.name, file)


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

    @patch('PyQt5.QtWidgets.QFileDialog.getOpenFileName',
           return_value=tmpConfig())
    def testLoadGame(self, openfile):
        self.game.loadGame()
        self.assertEqual(self.game.game.difficulty, 3)
        self.assertEqual(self.game.game.numberOfGames, 4)
        self.assertEqual(self.game.game.gamesPlayed, 1)
        self.assertEqual(self.game.game.playerScore, 3)
        self.assertEqual(self.game.game.opponentScore, 0)
        self.assertEqual(self.game.game.playerIsNotFirst, True)
