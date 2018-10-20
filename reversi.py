from board import *

# проверяет "валидность" хода - является ли он целым, и находится ли он 
# в множестве индексов всех клеток
def is_valid(move):
    return isinstance(move, int) and move in squares()

# возвращает цвет оппонента игрока 'player
def opponent(player):
    return BLACK if player is WHITE else WHITE

# находит первую клетку, которая формирует линию, начиная с заданной
# клетки 'square', для игрока 'player' в направлении 'direction'
def find_line(square, player, board, direction):
    line_index = square + direction
    if board[line_index] == player:
        return None
    opp = opponent(player)
    while board[line_index] == opp:
        line_index += direction
    return None if board[line_index] in (OUTER, EMPTY) else line_index

# проверяет возможность совершения хода 'move' игроком 'player'
# в соответствии правилам игры
def is_legal(move, player, board):
    has_line = lambda direction: find_line(move, player, board, direction)
    return board[move] == EMPTY and any(map(has_line, DIRECTIONS))

# Обновляет игровую доску в соответствии с ходом 'move' сделанным игроком 'player'
def make_move(move, player, board):
    board[move] = player
    for d in DIRECTIONS:
        make_flips(move, player, board, d)
    return board

# изменяет цвет всех клеток в результате хода 'move' игрока 'player'
def make_flips(move, player, board, direction):
    line = find_line(move, player, board, direction)
    if not line:
        return
    square = move + direction
    while square != line:
        board[square] = player
        square += direction

# Ошибка невозможного хода
class IllegalMoveError(Exception):
    def __init__(self, player, move, board):
        self.player = player
        self.move = move
        self.board = board

    def __str__(self):
        return '%s : невозможно совершить ход в клетку %d' % (PLAYERS[self.player], self.move)

# Возвращает список всех возможных ходов для игрока 'player'
def legal_moves(player, board):
    return [sq for sq in squares() if is_legal(sq, player, board)]

# Проверяет может ли игрок совершить хотя бы один ход
def any_legal_move(player, board):
    return any(is_legal(sq, player, board) for sq in squares())

# основная функция игры
# цикл, основанный на одном ходе игрока
# совершается ход, изменяется доска, передается право хода сопернику
# возвращает финальную доску и счет игры
def play(black_strategy, white_strategy):
    board = initial_board()
    player = BLACK
    strategy = lambda who: black_strategy if who == BLACK else white_strategy
    while player is not None:
        move = get_move(strategy(player), player, board)
        make_move(move, player, board)
        player = next_player(board, player)
    return board, score(BLACK, board)

# возвращает следующего игркоа
# если следующий игрок не сможет совершить ни одного хода, возвращает None
# в итоге это останавливает цикл игры play
def next_player(board, prev_player):
    opp = opponent(prev_player)
    if any_legal_move(opp, board):
        return opp
    elif any_legal_move(prev_player, board):
        return prev_player
    return None

# возвращает оптимальный ход игрока 'player' в соответствии с его стратегией 'strategy'
def get_move(strategy, player, board):
    copy = list(board)
    move = strategy(player, copy)
    if not is_valid(move) or not is_legal(move, player, board):
        raise IllegalMoveError(player, move, copy)
    return move

# счет - разница между захваченными тайлами игрока и его соперника
def score(player, board):
    my, opponents = 0, 0
    opp = opponent(player)
    for sq in squares():
        piece = board[sq]
        if piece == player: my += 1
        elif piece == opp: opponents += 1
    return my - opponents


# случайна стратегия
import random

# выбирает случайный ход из возможных
def random_strategy(player, board):
    return random.choice(legal_moves(player, board))

# максимальная стратегия

# A more sophisticated strategy could look at every available move and evaluate
# them in some way.  This consists of getting a list of legal moves, applying
# each one to a copy of the board, and choosing the move that results in the
# "best" board.

# стратегия, которая выбирает ход, максимизирующий значение функции evaluate
# например, можно передать score, и тогда на каждом шаге стратегия будет выбирать
# ход, приводящий к максимальному счету
def maximizer(evaluate):
    def strategy(player, board):
        def score_move(move):
            return evaluate(player, make_move(move, player, list(board)))
        return max(legal_moves(player, board), key=score_move)
    return strategy

SQUARE_WEIGHTS = [
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
    0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
    0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
    0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
    0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
    0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
    0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
    0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
]

# аналогично функции score, но счет высчитывается
# с учетом весов тайлов
def weighted_score(player, board):
    opp = opponent(player)
    total = 0
    for sq in squares():
        if board[sq] == player:
            total += SQUARE_WEIGHTS[sq]
        elif board[sq] == opp:
            total -= SQUARE_WEIGHTS[sq]
    return total

# минимакс


# в соответствии с заданной глубиной поиска 'depth' возвращает лучший возможных ход
# для игрока 'player'
def minimax(player, board, depth, evaluate):

    # "ценность" доски высчитывается как число противоположное ценности доски
    # соперника на его следующем ходе. Рекурсивный вызов minimax с углублением
    def value(board):
        return -minimax(opponent(player), board, depth-1, evaluate)[0]

    # при глубине 0 возвращаем полученное значение
    if depth == 0:
        return evaluate(player, board), None

    moves = legal_moves(player, board)
    if not moves:
        # если у игрока нет возможных ходов, поскольку их нет вообще
        # завершаем игру, возвращаем конечное значение доски
        if not any_legal_move(opponent(player), board):
            return final_value(player, board), None
        # либо просто пропускаем ход
        return value(board), None

    # если возможных ходы есть, возвращаем ход с максимальным значением
    return max((value(make_move(m, player, list(board))), m) for m in moves)

MAX_VALUE = sum(map(abs, SQUARE_WEIGHTS))
MIN_VALUE = -MAX_VALUE

# находит счет законченной игры
def final_value(player, board):
    diff = score(player, board)
    if diff < 0:
        return MIN_VALUE
    elif diff > 0:
        return MAX_VALUE
    return diff

# непосредственно стратегия, передаваемая в функцию play
def minimax_searcher(depth, evaluate):
    def strategy(player, board):
        return minimax(player, board, depth, evaluate)[1]
    return strategy

### Альфа-бета

# альфа - максимальный достижимый счет
# бета - минимальный счет, который будет достижим после хода соперника
# изначально альфа - минимальное значение, а бета - максимальное
# когда находится ход где альфа >= бета, мы прекращаем рассматривать эту ветвь дерева
def alphabeta(player, board, alpha, beta, depth, evaluate):
    # аналогично минимаксу, при дохождении до максимальной глубины, возвращает ценность
    if depth == 0:
        return evaluate(player, board), None
    
    def value(board, alpha, beta):
        # аналогично минимаксу, рекурсивный спуск
        # нас счет - отрицание счета соперника
        # альфа - лучший достижимый нами счет
        # бета - худший счет, который у нас может быть из-за хоад соперника
        return -alphabeta(opponent(player), board, -beta, -alpha, depth-1, evaluate)[0]

    moves = legal_moves(player, board)
    if not moves:
        if not any_legal_move(opponent(player), board):
            return final_value(player, board), None
        return value(board, alpha, beta), None

    best_move = moves[0]
    for move in moves:
        if alpha >= beta:
            # Ходы, где альфа > бета будут недопущены соперником
            break
        val = value(make_move(move, player, list(board)), alpha, beta)
        if val > alpha:
            # если один из ходов приводит к лучшему счету, чем текущий лучший, заменяем
            alpha = val
            best_move = move
    return alpha, best_move

# непосредственно стратегия, передаваемая в функцию play
def alphabeta_searcher(depth, evaluate):
    def strategy(player, board):
        return alphabeta(player, board, MIN_VALUE, MAX_VALUE, depth, evaluate)[1]
    return strategy