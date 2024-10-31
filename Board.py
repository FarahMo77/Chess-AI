"""The Board class consists of a simple 2D list to store the chess pieces
   and a number of required methods like make_move(), unmake_move() (which is necessary for the minimax algorithm),
   to check if the game is finished, and an evaluation method which returns the total score of the caller's pieces minus the
   total score of the opponent's pieces .
"""

from Chess_Pieces import *
from copy import deepcopy


class Board:
    whites = []
    blacks = []

    """
    Initializes a new Board object with the given game mode, AI, depth, and logging settings.
    Args:
    - game_mode (int): The game mode to use (0 for whites down/blacks up, 1 for blacks down/whites up).
    - ai (bool): Whether or not to use AI for the black player.
    - depth (int): The depth to use for the AI's search algorithm.
    - log (bool): Whether or not to log the game history.
    """

    def __init__(self, game_mode, ai=False, depth=2, log=False):
        self.board = []
        self.game_mode = game_mode
        self.depth = depth
        self.ai = ai
        self.log = log

    """
    Initializes the board with empty blocks.
    """

    def initialize_board(self):
        for i in range(8):
            self.board.append(['empty-block' for _ in range(8)])

    """
    Places the chess pieces on the board according to the standard starting position.
    """

    def place_pieces(self):
        self.board.clear()
        self.whites.clear()
        self.blacks.clear()
        self.initialize_board()
        self.whiteKing = King('white', 0, 4, '\u265A')
        self.blackKing = King('black', 7, 4, '\u2654')
        for j in range(8):
            self[1][j] = Pawn('white', 1, j, '\u265F')
            self[6][j] = Pawn('black', 6, j, '\u2659')
        self[0][0] = Rook('white', 0, 0, '\u265C')
        self[0][7] = Rook('white', 0, 7, '\u265C')
        self[0][1] = Knight('white', 0, 1, '\u265E')
        self[0][6] = Knight('white', 0, 6, '\u265E')
        self[0][2] = Bishop('white', 0, 2, '\u265D')
        self[0][5] = Bishop('white', 0, 5, '\u265D')
        self[0][3] = Queen('white', 0, 3, '\u265B')
        self[0][4] = self.whiteKing
        self[7][0] = Rook('black', 7, 0, '\u2656')
        self[7][7] = Rook('black', 7, 7, '\u2656')
        self[7][1] = Knight('black', 7, 1, '\u2658')
        self[7][6] = Knight('black', 7, 6, '\u2658')
        self[7][2] = Bishop('black', 7, 2, '\u2657')
        self[7][5] = Bishop('black', 7, 5, '\u2657')
        self[7][3] = Queen('black', 7, 3, '\u2655')
        self[7][4] = self.blackKing
        self.save_pieces()
        if self.game_mode != 0:
            self.reverse()

    """
    Saves the white and black pieces to their respective lists.
    """

    def save_pieces(self):
        for i in range(8):
            for j in range(8):
                if isinstance(self[i][j], ChessPiece):
                    if self[i][j].color == 'white':
                        self.whites.append(self[i][j])
                    else:
                        self.blacks.append(self[i][j])

    """
    Makes a move on the board by moving the given piece to the given position.
    Args:
    - piece (ChessPiece): The piece to move.
    - x (int): The x-coordinate of the position to move to.
    - y (int): The y-coordinate of the position to move to.
    - keep_history (bool): Whether to keep a log of the move for AI search purposes.
    """

    def make_move(self, piece, x, y, keep_history=False):
        old_x = piece.x
        old_y = piece.y
        if keep_history:
            self.board[old_x][old_y].set_last_eaten(self.board[x][y])
        else:
            if isinstance(self.board[x][y], ChessPiece):
                if self.board[x][y].color == 'white':
                    self.whites.remove(self.board[x][y])
                else:
                    self.blacks.remove(self.board[x][y])
        self.board[x][y] = self.board[old_x][old_y]
        self.board[old_x][old_y] = 'empty-block'
        self.board[x][y].set_position(x, y, keep_history)

    """
     Undoes the last move made on the board.
     Args:
     - piece (ChessPiece): The piece that was moved in the last move.
    """

    def unmake_move(self, piece):

        x = piece.x
        y = piece.y
        self.board[x][y].set_old_position()
        old_x = piece.x
        old_y = piece.y
        self.board[old_x][old_y] = self.board[x][y]
        self.board[x][y] = piece.get_last_eaten()

    """
    Reverses the board and updates the positions of the pieces accordingly.
    """

    def reverse(self):

        self.board = self.board[::-1]
        for i in range(8):
            for j in range(8):
                if isinstance(self.board[i][j], ChessPiece):
                    piece = self.board[i][j]
                    piece.x = i
                    piece.y = j

    """
    Returns the row of the board at the given index.
    Args:
     - item (int): The index of the row to return.
     Returns:
     - list: The row of the board at the given index.
    """

    def __getitem__(self, item):
        return self.board[item]

    """
    Checks if the given position contains an opponent's piece.
     Args:
    - piece (ChessPiece): The piece to check for opponents.
    - x (int): The x-coordinate of the position to check.
    - y (int): The y-coordinate of the position to check.
    Returns:
    - bool: True if the position contains an opponent's piece, False otherwise.
    """

    def has_opponent(self, piece, x, y):

        if not self.is_valid_move(x, y):
            return False
        if isinstance(self.board[x][y], ChessPiece):
            return piece.color != self[x][y].color
        return False

    """
    Checks if the given position contains a friendly piece.
    Args:
    - piece (ChessPiece): The piece to check for friends.
    - x (int): The x-coordinate of the position to check.
    - y (int): The y-coordinate of the position to check.
    Returns:
    - bool: True if the position contains a friendly piece, False otherwise.
    """

    def has_friend(self, piece, x, y):

        if not self.is_valid_move(x, y):
            return False
        if isinstance(self[x][y], ChessPiece):
            return piece.color == self[x][y].color
        return False

    """
    Checks if the given position is a valid position on the board.
     Args:
     - x (int): The x-coordinate of the position to check.
     - y (int): The y-coordinate of the position to check.
     Returns:
    - bool: True if the position is valid, False otherwise.
    """

    def is_valid_move(self, x, y):

        return x >= 0 and x < 8 and y >= 0 and y < 8

    """
     Checks if the given position is a valid position on the board.
     Args:
     - x (int): The x-coordinate of the position to check.
     - y (int): The y-coordinate of the position to check.
     Returns:
     - bool: True if the position is valid, False otherwise.
            """

    @staticmethod
    def is_valid_move(x, y):
        return 0 <= x < 8 and 0 <= y < 8

    def has_empty_block(self, x, y):
        """
        Checks if the given position is empty.

        Args:
        - x (int): The x-coordinate of the position to check.
        - y (int): The y-coordinate of the position to check.

        Returns:
        - bool: True if the position is empty, False otherwise.
        """
        if not self.is_valid_move(x, y):
            return False
        return not isinstance(self[x][y], ChessPiece)

    """
    Returns the color of the current player.
    Returns:
    -The color of the current player ('white' or 'black').
     """

    def get_player_color(self):
        if self.game_mode == 0:
            return 'white'
        return 'black'

    """
    Checks if the given color's king is threatened by any of the opponent's pieces.
    Args:
     - color (str): The color of the king to check ('white' or 'black').
     - move (tuple): The move that was just made, if any.
      Returns:
      - bool: True if the king is threatened, False otherwise.
    """

    def king_is_threatened(self, color, move=None):

        if color == 'white':
            enemies = self.blacks
            king = self.whiteKing
        else:
            enemies = self.whites
            king = self.blackKing
        threats = []
        for enemy in enemies:
            moves = enemy.get_moves(self)
            if (king.x, king.y) in moves:
                threats.append(enemy)
        if move and len(threats) == 1 and threats[0].x == move[0] and threats[0].y == move[1]:
            return False
        return True if len(threats) > 0 else False

    """
    Checks if the game has reached a terminal state (i.e. one player has won or there are no more moves).
    Returns:
    - bool: True if the game is in a terminal state, False otherwise.
    """

    def is_terminal(self):
        terminal1 = self.white_won()
        terminal2 = self.black_won()
        return terminal1 or terminal2

    """
    Checks if the white player has won the game.
    Returns:
    - bool: True if the white player has won, False otherwise.
    """

    def white_won(self):
        if self.king_is_threatened('black') and not self.has_moves('black'):
            return True
        return False

    """
    Checks if the black player has won the game.
    Returns:
    - bool: True if the black player has won, False otherwise.
    """

    def black_won(self):
        if self.king_is_threatened('white') and not self.has_moves('white'):
            return True
        return False

    """
    Checks if the given color has any valid moves.
    Args:
     - color (str): The color of the player to check ('white' or 'black').
    Returns:
    - bool: True if the player has valid moves, False otherwise.
    """

    def has_moves(self, color):
        total_moves = 0
        for i in range(8):
            for j in range(8):
                if isinstance(self[i][j], ChessPiece) and self[i][j].color == color:
                    piece = self[i][j]
                    total_moves += len(piece.filter_moves(piece.get_moves(self), self))
                    if total_moves > 0:
                        return True
        return False

    """
    Evaluates the current state of the board and returns a score.
    Returns:
    - int: The score of the current state of the board.
    """

    def evaluate(self):

        white_points = 0
        black_points = 0
        for i in range(8):
            for j in range(8):
                if isinstance(self[i][j], ChessPiece):
                    piece = self[i][j]
                    if piece.color == 'white':
                        white_points += piece.get_score()
                    else:
                        black_points += piece.get_score()
        if self.game_mode == 0:
            return black_points - white_points
        return white_points - black_points

    """
    Returns a 2D array of Unicode characters representing the current state of the board.
    Returns:
    - list: A 2D array of Unicode characters representing the current state of the board.
    """

    def unicode_array_repr(self):
        data = deepcopy(self.board)
        for idx, row in enumerate(self.board):
            for i, p in enumerate(row):
                if isinstance(p, ChessPiece):
                    un = p.unicode
                else:
                    un = '\u25AF'
                data[idx][i] = un
        return data[::-1]

    """
    Returns the king of the same color as the given piece.
    Args:
    - piece (ChessPiece): The piece to get the king for.
    Returns:
    - King: The king of the same color as the given piece.
    """

    def get_king(self, piece):
        if piece.color == 'white':
            return self.whiteKing
        return self.blackKing
