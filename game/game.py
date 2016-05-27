from . import boards


class Game:
    def __init__(self, player1, player2):
        self.macroboard = boards.Macroboard()
        self.players = [player1, player2]
        self.on_turn = 0

    def start(self):
        while self.macroboard.state == boards.State.IN_PROGRESS:
            print(self.macroboard)
            move = self.players[self.on_turn].choose_move(self.macroboard)
            self.macroboard.make_move(*move)
            self.on_turn = abs(self.on_turn - 1)
        print(self.macroboard)
