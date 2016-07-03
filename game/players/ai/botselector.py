from .euristicsbot import EuristicsBot


def select_bot(difficulty):
    if difficulty == 1:
        return EuristicsBot('Euristics bot')
    elif difficulty == 2:
        return EuristicsBot('Euristics bot')
    elif difficulty == 3:
        return EuristicsBot('Euristics bot')
    elif difficulty == 4:
        return EuristicsBot('Euristics bot')
    else:
        raise ValueError('No such difficulty.')
