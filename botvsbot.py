from ultimatetictactoe import game
from collections import Counter


def one_game_result():
    bot1 = game.players.ai.HeuristicsBot('B1')
    # bot2 = game.players.ai.heuristicsbot.EuristicsBot('B2')
    bot2 = game.players.ai.RandomBot('B2')
    on_turn = bot1
    board = game.boards.Macroboard()
    while board.state == game.boards.State.IN_PROGRESS:
        move = on_turn.choose_move(board)
        board.make_move(*move)
        on_turn = bot1 if on_turn == bot2 else bot2
    return board.state


def n_games_result(n):
    results = []
    for _ in range(n):
        print(_)
        results.append(one_game_result())
        print(Counter(results))
    return Counter(results)


if __name__ == '__main__':
    print(n_games_result(10))
