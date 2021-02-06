"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state(): # starting 3x3 board
    return [[EMPTY, EMPTY, EMPTY] for i in range(3)]

def player(board):
    # Returns player who has the next turn on a board.
    return X if sum(x.count("X") for x in board) == sum(x.count("O") for x in board) else O

def actions(board):
    # Returns set of all possible actions (i, j) available on the board.
    action = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                action.append((i, j))
    return action

def result(board, action):
    # Returns the board that results from making move (i, j) on the board.
    board = copy.deepcopy(board)
    i, j = action
    if board[i][j] == EMPTY:
        board[i][j] = player(board)
        return board
    raise Exception("Invalid move")

def winner(board):
    # Returns the winner of the game, if there is one.
    # For X
    if board[0] == ["X", "X", "X"] or board[1] == ["X", "X", "X"] or board[2] == ["X", "X", "X"]\
            or (board[0][0] == "X" and board[1][0] == "X" and board[2][0] == "X")\
            or (board[0][1] == "X" and board[1][1] == "X" and board[2][1] == "X")\
            or (board[0][2] == "X" and board[1][2] == "X" and board[2][2] == "X")\
            or (board[0][0] == "X" and board[1][1] == "X" and board[2][2] == "X")\
            or (board[0][2] == "X" and board[1][1] == "X" and board[2][0] == "X"):
        return X

    # For O
    if board[0] == ["O", "O", "O"] or board[1] == ["O", "O", "O"] or board[2] == ["O", "O", "O"]\
            or (board[0][0] == "O" and board[1][0] == "O" and board[2][0] == "O")\
            or (board[0][1] == "O" and board[1][1] == "O" and board[2][1] == "O")\
            or (board[0][2] == "O" and board[1][2] == "O" and board[2][2] == "O")\
            or (board[0][0] == "O" and board[1][1] == "O" and board[2][2] == "O")\
            or (board[0][2] == "O" and board[1][1] == "O" and board[2][0] == "O"):
        return O

def terminal(board):
    # Is the game over?
    return True if sum(x.count(EMPTY) for x in board) == 0 or winner(board) else False

def utility(board):
    # Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0

def minimax(board):
    if player(board) == X:
        v = -math.inf
        for action in actions(board):
            v_op = minVal(result(board, action)) 
            if v_op > v:
                v = v_op
                optimal_move = action
    else:
        v = math.inf
        for action in actions(board):
            v_op = maxVal(result(board, action)) 
            if v_op < v:
                v = v_op
                optimal_move = action
    return optimal_move

def maxVal(board): # Maximizing function for X
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, minVal(result(board, action)))
    return v    

def minVal(board): # Minimizing function for O
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, maxVal(result(board, action)))
    return v  
