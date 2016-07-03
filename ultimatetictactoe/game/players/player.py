class Player:
    def __init__(self, name):
        self.name = name

    def choose_move(self, macroboard):
        raise NotImplementedError

    def set_name(self, name):
        self.name = name
