from ultimatetictactoe import game
import datetime


def one_game_time():
    bot1 = game.players.ai.HeuristicsBot('B1')
    bot2 = game.players.ai.RandomBot('B2')
    bot1.time = 0
    bot2.time = 0
    bot1.moves = 0
    bot2.moves = 0
    on_turn = bot1
    board = game.boards.Macroboard()
    while board.state == game.boards.State.IN_PROGRESS:

        t1 = datetime.datetime.now()
        move = on_turn.choose_move(board)
        delta = datetime.datetime.now() - t1
        on_turn.time += delta.total_seconds()
        on_turn.moves += 1

        board.make_move(*move)
        on_turn = bot1 if on_turn == bot2 else bot2
    return (bot1.time, bot1.moves)


if __name__ == '__main__':
    print(one_game_time())
