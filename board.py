from colorama import Fore
from color import *

# Черный: Ч, Белый: Б, Пустой: ., Граничный: #
EMPTY = '.'
BLACK = colorize('Ч', Fore.BLUE)
WHITE = colorize('Б', Fore.WHITE)
OUTER = colorize('#', Fore.RED)
# Все виды тайлов
PIECES = (EMPTY, BLACK, WHITE, OUTER)
# Игроки
PLAYERS = {BLACK: 'Black', WHITE: 'White'}


#Индексы обращения к соседним клеткам. Работает, поскольку игровая доска - список
UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)

#Возвращает индексы всех клеток, генератор
def squares():
    return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]

#Создает доску, инициализирует начальное состояние игры
def initial_board():
    board = [OUTER] * 100
    for i in squares():
        board[i] = EMPTY
    # The middle four squares should hold the initial piece positions.
    board[44], board[45] = WHITE, BLACK
    board[54], board[55] = BLACK, WHITE
    return board

#Вывод игровой доски в консоль
def print_board(board):
    repr = ''
    repr += '  %s\n' % ' '.join(map(lambda x: colorize(str(x), Fore.RED), range(1, 9)))
    for row in range(1, 9):
        begin, end = 10 * row + 1, 10 * row + 9
        repr += '%s %s\n' % (colorize(str(row), Fore.RED), ' '.join(board[begin:end]))
    return repr
