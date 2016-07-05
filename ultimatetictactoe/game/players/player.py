class Player:
    """
    Abstraction of a game player.
    """
    def __init__(self, name):
        self.name = name

    def choose_move(self, macroboard):
        """
        Accepts a Macroboard object and returns a valid move for it.
        Must be overriden.
        """
        raise NotImplementedError

    def set_name(self, name):
        self.name = name
