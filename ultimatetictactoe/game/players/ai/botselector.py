from .heuristicsbot import HeuristicsBot


def select_bot(difficulty):
    if difficulty == 1:
        return HeuristicsBot('Euristics bot')
    elif difficulty == 2:
        return HeuristicsBot('Euristics bot')
    elif difficulty == 3:
        return HeuristicsBot('Euristics bot')
    elif difficulty == 4:
        return HeuristicsBot('Euristics bot')
    else:
        raise ValueError('No such difficulty.')
