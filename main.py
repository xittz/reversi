from reversi import *
from color import *
from colorama import Fore, Style

# проверка введенного человеком хода
def check(move, player, board):
    return is_valid(move) and is_legal(move, player, board)

# запрос данных о ходе человека
def human_move(player, board):
    print(print_board(board))
    print('Ваш ход:')
    while True:
        move = input('> ')
        if move and check(int(move), player, board):
            return int(move)
        elif move:
            print('Невозможно совершить данный ход. Попробуйте снова')

# выбор стратегии из списка
def choose_strategy(prompt, strategies):
    print(prompt)
    print('Стратегии:', list(strategies.keys()))
    while True:
        choice = input('> ')
        if choice in strategies:
            return strategies[choice]
        elif choice:
            print('Неверный выбор')

# инициализация игроков - выбор стратегий
def init_players():
    print(dim(colorize('\nИгра Реверси\n', Fore.GREEN)))
    strategies = { 'человек': human_move,
                'случайная': random_strategy,
                'maximize': maximizer(score),
                'weighted-maximize': maximizer(weighted_score),
                'minimax': minimax_searcher(3, score),
                'weighted-minimax':
                    minimax_searcher(3, weighted_score),
                'alphabeta': alphabeta_searcher(3, score),
                'weighted-alphabeta':
                    alphabeta_searcher(3, weighted_score) }
    black = choose_strategy('Черный - выбери стратегию', strategies)
    print('\n')
    white = choose_strategy('Белый - выбери стратегию', strategies)
    print('\n')
    return black, white

# инициализация игры
def init_game():
    try:
        black, white = init_players()
        board, score = play(black, white)
    except IllegalMoveError as e:
        print(e)
        return
    except EOFError as e:
        print(e)
        return
    if score > 0:
        print('Итоговый счет: ' + Fore.GREEN + str(score) + Fore.WHITE)
    else:
        print('Итоговый счет: ' + Fore.RED + str(score) + Fore.WHITE)
    print('%s выиграл!' % ('Черный' if score > 0 else 'Белый'))
    print(print_board(board))


if __name__ == "__main__":
    init_game()
