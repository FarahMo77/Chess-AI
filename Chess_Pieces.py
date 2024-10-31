""" The ChessPiece class is an abstract class and it is used as a parent for every piece.
    It consists of a method for moves filtering (prevent illegal moves like exposing the king) and some methods to keep
    the previous state of the chess piece intact (required by the ai when calling unmake_move()).
    Every chess piece is equipped with a get_score() function that is used when evaluating the board.
    The scores are 10 points for the pawns, 20 for knights, 30 for bishops and rooks, 240 for the queen and 1000 for the king.
"""


import operator  # Import the operator module
from itertools import product  # Import the product function from the itertools module

class ChessPiece:

    # history is used to keep data, so board.unmake_move() works properly.
    eaten_pieces_history = []  # A list to keep track of the pieces eaten by this piece
    has_moved_history = []  # A list to keep track of whether this piece has moved
    position_history = []  # A list to keep track of the previous positions of this piece

    def __init__(self, color, x, y, unicode):
        self.moved = False  # Whether this piece has moved
        self.color = color  # The color of this piece
        self.x = x  # The x-coordinate of this piece on the board
        self.y = y  # The y-coordinate of this piece on the board
        self.type = self.__class__.__name__  # The type of this piece (e.g. 'Pawn', 'Knight', etc.)
        self.unicode = unicode  # The Unicode character used to represent this piece on the board

    def filter_moves(self, moves, board):
        final_moves = moves[:]  # Create a copy of the moves list
        for move in moves:
            board.make_move(self, move[0], move[1], keep_history=True)  # Make the move on the board
            if board.king_is_threatened(self.color, move):  # Check if the move puts the king in check
                final_moves.remove(move)  # Remove the move from the list of valid moves
            board.unmake_move(self)  # Undo the move on the board
        return final_moves  # Return the list of valid moves

    def get_moves(self, board):
        pass  # This method is overridden by subclasses

    def get_last_eaten(self):
        return self.eaten_pieces_history.pop()  # Remove and return the last piece eaten by this piece

    def set_last_eaten(self, piece):
        self.eaten_pieces_history.append(piece)  # Add a piece to the list of pieces eaten by this piece

    def set_position(self, x, y, keep_history):
        if keep_history:
            self.position_history.append(self.x)  # Add the current x-coordinate to the position history list
            self.position_history.append(self.y)  # Add the current y-coordinate to the position history list
            self.has_moved_history.append(self.moved)  # Add the current moved status to the has_moved_history list
        self.x = x  # Set the new x-coordinate
        self.y = y  # Set the new y-coordinate
        self.moved = True  # Set the moved status to True

    def set_old_position(self):
        position_y = self.position_history.pop()  # Get the previous y-coordinate from the position history list
        position_x = self.position_history.pop()  # Get the previous x-coordinate from the position history list
        self.y = position_y  # Set the y-coordinate to the previous value
        self.x = position_x  # Set the x-coordinate to the previous value
        self.moved = self.has_moved_history.pop()  # Set the moved status to the previous value

    def get_score(self):
        return 0  # This method is overridden by subclasses

    def __repr__(self):
        return '{}: {}|{},{}'.format(self.type, self.color, self.x, self.y)  # Return a string representation of this piece

class Pawn(ChessPiece):

    def get_moves(self, board):
        moves = []
        if board.game_mode == 0 and self.color == 'white' or board.game_mode == 1 and self.color == 'black':
            direction = 1  # The direction in which the pawn moves
        else:
            direction = -1
        x = self.x + direction
        if board.has_empty_block(x, self.y):
            moves.append((x, self.y))
            if self.moved is False and board.has_empty_block(x + direction, self.y):
                moves.append((x + direction, self.y))
        if board.is_valid_move(x, self.y - 1):
            if board.has_opponent(self, x, self.y - 1):
                moves.append((x, self.y - 1))
        if board.is_valid_move(self.x + direction, self.y + 1):
            if board.has_opponent(self, x, self.y + 1):
                moves.append((x, self.y + 1))
        return moves

    def get_score(self):
        return 10  # Return the score of this piece


class Knight(ChessPiece):

    def get_moves(self, board):
        moves = []
        add = operator.add  # The add function from the operator module
        sub = operator.sub  # The subtract function from the operator module
        op_list = [(add, sub), (sub, add), (add, add), (sub, sub)]  # A list of tuples representing the possible moves
        nums = [(1, 2), (2, 1)]  # A list of tuples representing the possible distances
        combinations = list(product(op_list, nums))  # A list of tuples representing all possible combinations of moves and distances
        for comb in combinations:
            x = comb[0][0](self.x, comb[1][0])  # Calculate the new x-coordinate
            y = comb[0][1](self.y, comb[1][1])  # Calculate the new y-coordinate
            if board.has_empty_block(x, y) or board.has_opponent(self, x, y):
                moves.append((x, y))
        return moves

    def get_score(self):
        return 20  # Return the score of this piece


class Bishop(ChessPiece):

    def get_moves(self, board):
        moves = []
        add = operator.add  # The add function from the operator module
        sub = operator.sub  # The subtract function from the operator module
        operators = [(add, add), (add, sub), (sub, add), (sub, sub)]  # A list of tuples representing the possible moves
        for ops in operators:
            for i in range(1, 9):
                x = ops[0](self.x, i)  # Calculate the new x-coordinate
                y = ops[1](self.y, i)  # Calculate the new y-coordinate
                if not board.is_valid_move(x, y) or board.has_friend(self, x, y):  # Check if the move is valid or if there is a friendly piece in the way
                    break  # Stop checking this direction if the move is invalid or if there is a friendly piece in the way
                if board.has_empty_block(x, y):  # Check if the block is empty
                    moves.append((x, y))  # Add the move to the list of valid moves
                if board.has_opponent(self, x, y):  # Check if there is an opponent piece on the block
                    moves.append((x, y))  # Add the move to the list of valid moves
                    break  # Stop checking this direction if there is an opponent piece on the block
        return moves  # Return the list of valid moves

    def get_score(self):
        return 30  # Return the score of this piece


class Rook(ChessPiece):

    def get_moves(self, board):
        moves = []
        moves += self.get_vertical_moves(board)  # Get the vertical moves
        moves += self.get_horizontal_moves(board)  # Get the horizontal moves
        return moves  # Return the list of valid moves

    def get_vertical_moves(self, board):
        moves = []
        for op in [operator.add, operator.sub]:  # Iterate over the add and subtract functions
            for i in range(1, 9):
                x = op(self.x, i)  # Calculate the new x-coordinate
                if not board.is_valid_move(x, self.y) or board.has_friend(self, x, self.y):  # Check if the move is valid or if there is a friendly piece in the way
                    break  # Stop checking this direction if the move is invalid or if there is a friendly piece in the way
                if board.has_empty_block(x, self.y):  # Check if the block is empty
                    moves.append((x, self.y))  # Add the move to the list of valid moves
                if board.has_opponent(self, x, self.y):  # Check if there is an opponent piece on the block
                    moves.append((x, self.y))  # Add the move to the list of valid moves
                    break  # Stop checking this direction if there is an opponent piece on the block
        return moves  # Return the list of valid moves

    def get_horizontal_moves(self, board):
        moves = []
        for op in [operator.add, operator.sub]:  # Iterate over the add and subtract functions
            for i in range(1, 9):
                y = op(self.y, i)  # Calculate the new y-coordinate
                if not board.is_valid_move(self.x, y) or board.has_friend(self, self.x, y):  # Check if the move is valid or if there is a friendly piece in the way
                    break  # Stop checking this direction if the move is invalid or if there is a friendly piece in the way
                if board.has_empty_block(self.x, y):  # Check if the block is empty
                    moves.append((self.x, y))  # Add the move to the list of valid moves
                if board.has_opponent(self, self.x, y):  # Check if there is an opponent piece on the block
                    moves.append((self.x, y))  # Add the move to the list of valid moves
                    break  # Stop checking this direction if there is an opponent piece on the block
        return moves  # Return the list of valid moves

    def get_score(self):
        return 30  # Return the score of this piece


class Queen(ChessPiece):

    def get_moves(self, board):
        moves = []
        rook = Rook(self.color, self.x, self.y, self.unicode)  # Create a new Rook object
        bishop = Bishop(self.color, self.x, self.y, self.unicode)  # Create a new Bishop object
        rook_moves = rook.get_moves(board)  # Get the valid moves for the Rook
        bishop_moves = bishop.get_moves(board)  # Get the valid moves for the Bishop
        if rook_moves:
            moves.extend(rook_moves)  # Add the Rook moves to the list of valid moves
        if bishop_moves:
            moves.extend(bishop_moves)  # Add the Bishop moves to the list of valid moves
        return moves  # Return the list of valid moves

    def get_score(self):
        return 240  # Return the score of this piece


class King(ChessPiece):

    def get_moves(self, board):
        moves = []
        moves += self.get_horizontal_moves(board)  # Get the horizontal moves
        moves += self.get_vertical_moves(board)  # Get the vertical moves
        return moves  # Return the list of valid moves

    def get_vertical_moves(self, board):
        moves = []
        for op in [operator.add, operator.sub]:  # Iterate over the add and subtract functions
            x = op(self.x, 1)  # Calculate the new x-coordinate
            if board.has_empty_block(x, self.y) or board.has_opponent(self, x, self.y):  # Check if the block is empty or if there is an opponent piece on the block
                moves.append((x, self.y))  # Add the move to the list of valid moves
            if board.has_empty_block(x, self.y + 1) or board.has_opponent(self, x, self.y + 1):  # Check if the block is empty or if there is an opponent piece the block
                moves.append((x, self.y+1))  # Add the move to the list of valid moves
            if board.has_empty_block(x, self.y - 1) or board.has_opponent(self, x, self.y - 1):  # Check if the block is empty or if there is an opponent piece on the block
                moves.append((x, self.y - 1))  # Add the move to the list of valid moves
        return moves  # Return the list of valid moves

    def get_horizontal_moves(self, board):
        moves = []
        for op in [operator.add, operator.sub]: # Iterate over the add and subtract functions
            y = op(self.y, 1)
            if board.has_empty_block(self.x, y) or board.has_opponent(self, self.x, y): # Check if the block is empty or if there is an opponent piece the block
                moves.append((self.x, y)) # Add the move to the list of valid moves
        return moves # Return the list of valid moves

    ''' The get_score method returns a high score for the king, which reflects its importance in the game.
       This score is used by the AI to evaluate the board.
    '''
    def get_score(self):
        return 1000
