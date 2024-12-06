"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    turnX = 0
    turnO = 0

    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                turnX += 1
            elif board[i][j] == O:
                turnO += 1
    # X=O X turn
    # X>O O turn

    if turnX == turnO:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # create the set
    actions = set()

    # iterate over board

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    copy = deepcopy(board)
    if copy[action[0]][action[1]] == EMPTY:
        copy[action[0]][action[1]] = player(board)
    else:
        raise ValueError
    return copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Loop through board
    for i in range(3):  # vertical combos
        if board[i][0] == board[i][1] == board[i][2]:
            if board[i][0] != EMPTY:
                return board[i][0]

    for j in range(3):  # horizontal combos
        if board[0][j] == board[1][j] == board[2][j]:
            if board[0][j] != EMPTY:
                return board[0][j]

    if board[0][0] == board[1][1] == board[2][2]:  # diagonal combos
        if board[0][0] != EMPTY:
            return board[0][0]

    if board[2][0] == board[1][1] == board[0][2]:
        if board[2][0] != EMPTY:
            return board[2][0]

    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    turns = 0

    for i in range(3):
        for j in range(3):
            if board[i][j] != EMPTY:
                turns += 1

    if winner(board) != None:
        return True

    elif turns == 9:
        return True

    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minval(board):
    """
    Returns the minimal value option of maximal value options.
    """
    if terminal(board):
        return utility(board)  # make sure not Game Over

    value = float('inf')

    for action in actions(board):
        value = min(value, maxval(result(board, action)))
    return value


def maxval(board):
    """
    Returns the maximal value option of minimum value results.
    """
    if terminal(board):
        return utility(board)  # make sure not Game Over

    value = -float('inf')

    for action in actions(board):
        value = max(value, minval(result(board, action)))
    return value


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # look for optimal moves
    if terminal(board):
        return None

    elif player(board) == X:  # X wants highest value
        moves = []
        for action in actions(board):
            score = minval(result(board, action))
            moves.append([score, action])
        return sorted(moves, reverse=True)[0][1]  # max value option

    elif player(board) == O:
        moves = []
        for action in actions(board):
            score = maxval(result(board, action))
            moves.append([score, action])

        return sorted(moves)[0][1]  # min value option
