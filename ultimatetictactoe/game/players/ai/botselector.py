from .alphabetabot import AlphaBetaBot
from .heuristicsbot import HeuristicsBot
from .randombot import RandomBot
from .gentlemanbot import GentlemanBot


def select_bot(difficulty):
    if difficulty == 1:
        return GentlemanBot('Gentleman bot')
    elif difficulty == 2:
        return RandomBot('Random bot')
    elif difficulty == 3:
        return HeuristicsBot('Heuristics bot')
    elif difficulty == 4:
        return AlphaBetaBot('AlphaBeta bot')
    else:
        raise ValueError('No such difficulty.')
