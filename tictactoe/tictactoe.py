"""
Tic Tac Toe Player
"""

import math
import numpy as np
import copy


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
    board = np.array(board)
    board = board.flatten()
    empties = (board == EMPTY).sum()

    return X if empties % 2 != 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    actions = set()
    for y in range(3):
        for x in range(3):
            if board[y][x] is EMPTY:
                actions.add((y, x))

    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    p = player(board)
    result_board = copy.deepcopy(board)
    try :
        square = result_board[action[0]][action[1]] 
        if square is EMPTY: 
            result_board[action[0]][action[1]] = p 
        else: 
            raise InvalidActionError
    except IndexError:
        raise InvalidActionError
    return result_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if set(row).__len__() == 1 and row[0] is not EMPTY:
            return row[0]
    for i in range(3):
        if board[0][i] == board [1][i] and board [1][i] == board[2][i]:
            return board[0][i]
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]
    if board[2][0] == board[1][1] and board[1][1] == board[0][2]:
        return board[2][0]
    
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    
    board = np.array(board)
    board = board.flatten()
    empties = (board == EMPTY).sum()

    return True if empties == 0 else False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result = winner(board)
    if result == X:
        return 1
    elif result == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None    

    value = 1 if player(board) == X else -1
    moves = {}
    for action in actions(board):
        board_after_action = result(board, action)
        if value == -1:
            best_outcome = maxValue(board_after_action)
            moves[best_outcome] = action
        else:
            moves[minValue(board_after_action)] = action
    return moves.get(value) if moves.get(value) else moves.get(0)


def maxValue(board):
    if terminal(board):
        return utility(board)
    v = -2
    for action in actions(board):
        v = max(v, minValue(result(board, action)))
        if v == 1:
            return 1
    return v

def minValue(board):
    if terminal(board):
        return utility(board)
    v = 2
    for action in actions(board):
        v = min(v, maxValue(result(board, action)))
        if v == -1:
            return -1
    return v

class InvalidActionError(Exception):
    "Invalid Action"
    pass