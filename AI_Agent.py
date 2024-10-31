''' AI_Agent class is a static class and it is used to get a move from the computer. There is a method that returns a
    random move and a method that returns an ai move using the minimax alogirthm.
'''
import math
from Board import Board
from Chess_Pieces import *
from functools import wraps
from Logger import Logger, BoardRepr
import random

# The logger = Logger() statement creates an instance of the Logger class, which will be used to log the game tree.
logger = Logger()

''' The log_tree function is a decorator function that takes a function as an argument and returns a wrapper function.
   The wrapper function logs the game tree if logging is enabled and then calls the original function with the same arguments.
   The wraps decorator is used to preserve the metadata of the original function  in the wrapper function.
'''
def log_tree(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        board: Board = args[0]
        if board.log:
            depth = args[1]
            write_to_file(board, depth)
        return func(*args, **kwargs)
    return wrapper


# Function to write the current board state to the log file
def write_to_file(board: Board, current_depth):
    global logger
    if board.depth == current_depth:
        logger.clear()
    board_repr = BoardRepr(board.unicode_array_repr(), current_depth, board.evaluate())
    logger.append(board_repr)


# Minimax algorithm with alpha-beta pruning
# the @log_tree syntax is used apply the log_tree decorator to the minimax function
@log_tree
def minimax(board, depth, alpha, beta, max_player, save_move, data):
    # Base case: if the maximum depth is reached or the game is over, return the evaluation of the board
    if depth == 0 or board.is_terminal():
        data[1] = board.evaluate()
        return data

    if max_player:
        max_eval = -math.inf
        for i in range(8):
            for j in range(8):
                # Check if the current piece belongs to the opponent
                if isinstance(board[i][j], ChessPiece) and board[i][j].color != board.get_player_color():
                    piece = board[i][j]
                    # Filter the moves of the piece based on the current board state
                    moves = piece.filter_moves(piece.get_moves(board), board)
                    for move in moves:
                        # Make the move and evaluate the resulting board state
                        board.make_move(piece, move[0], move[1], keep_history=True)
                        evaluation = minimax(board, depth - 1, alpha, beta, False, False, data)[1]
                        # Save the move if it has the highest evaluation so far
                        if save_move:
                            if evaluation >= max_eval:
                                if evaluation > data[1]:
                                    data.clear()
                                    data[1] = evaluation
                                    data[0] = [piece, move, evaluation]
                                elif evaluation == data[1]:
                                    data[0].append([piece, move, evaluation])
                        # Undo the move and update alpha and max_eval
                        board.unmake_move(piece)
                        max_eval = max(max_eval, evaluation)
                        alpha = max(alpha, evaluation)
                        if beta <= alpha:
                            break
        return data
    else:
        min_eval = math.inf
        for i in range(8):
            for j in range(8):
                # Check if the current piece belongs to the player
                if isinstance(board[i][j], ChessPiece) and board[i][j].color == board.get_player_color():
                    piece = board[i][j]
                    # Get all the moves of the piece
                    moves = piece.get_moves(board)
                    for move in moves:
                        # Make the move and evaluate the resulting board state
                        board.make_move(piece, move[0], move[1], keep_history=True)
                        evaluation = minimax(board, depth - 1, alpha, beta, True, False, data)[1]
                        # Undo the move and update beta and min_eval
                        board.unmake_move(piece)
                        min_eval = min(min_eval, evaluation)
                        beta = min(beta, evaluation)
                        if beta <= alpha:
                            break
        return data


# Function to get the AI's move
def get_ai_move(board):
    # Run the minimax algorithm to get the best move
    moves = minimax(board, board.depth, -math.inf, math.inf, True, True, [[], 0])
    # Write the game tree to the log file if logging is enabled
    if board.log:
        logger.write()
    # Choose a random move if there are no possible moves
    if len(moves[0]) == 0:
        return False
    # Choose the move with the highest evaluation
    best_score = max(moves[0], key=lambda x: x[2])[2]
    piece_and_move = random.choice([move for move in moves[0] if move[2] == best_score])
    piece = piece_and_move[0]
    move = piece_and_move[1]
    # Make the move on the board
    if isinstance(piece, ChessPiece) and len(move) > 0 and isinstance(move, tuple):
        board.make_move(piece, move[0], move[1])
    return True

# Function to get a random move
def get_random_move(board):
    pieces = []
    moves = []
    for i in range(8):
        for j in range(8):
            # Check if the current piece belongs to the opponent
            if isinstance(board[i][j], ChessPiece) and board[i][j].color != board.get_player_color():
                pieces.append(board[i][j])
    for piece in pieces[:]:
        # Filter the moves of the piece based on the current board state
        piece_moves = piece.filter_moves(piece.get_moves(board), board)
        if len(piece_moves) == 0:
            pieces.remove(piece)
        else:
            moves.append(piece_moves)
    # Choose a random piece and move
    if len(pieces) == 0:
        return
    piece = random.choice(pieces)
    move = random.choice(moves[pieces.index(piece)])
    # Make the move on the board
    if isinstance(piece, ChessPiece) and len(move) > 0:
        board.make_move(piece, move[0], move[1])
