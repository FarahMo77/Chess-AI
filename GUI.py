# Importing the necessary modules
import pygame
from Chess_Pieces import *
from AI_Agent import get_random_move, get_ai_move
dark_block = pygame.image.load('images/Chess/128px/square black_png_shadow_128px.png')
light_block = pygame.image.load('images/Chess/128px/square white_png_shadow_128px.png')
dark_block = pygame.transform.scale(dark_block, (75, 75))
light_block = pygame.transform.scale(light_block, (75, 75))
whitePawn = pygame.image.load('images/Chess/128px/w_pawn_png_shadow_128px.png')
whitePawn = pygame.transform.scale(whitePawn, (75, 75))
whiteRook = pygame.image.load('images/Chess/128px/w_rook_png_shadow_128px.png')
whiteRook = pygame.transform.scale(whiteRook, (75, 75))
whiteBishop = pygame.image.load('images/Chess/128px/w_bishop_png_shadow_128px.png')
whiteBishop = pygame.transform.scale(whiteBishop, (75, 75))
whiteKnight = pygame.image.load('images/Chess/128px/w_knight_png_shadow_128px.png')
whiteKnight = pygame.transform.scale(whiteKnight, (75, 75))
whiteKing = pygame.image.load('images/Chess/128px/w_king_png_shadow_128px.png')
whiteKing = pygame.transform.scale(whiteKing, (75, 75))
whiteQueen = pygame.image.load('images/Chess/128px/w_queen_png_shadow_128px.png')
whiteQueen = pygame.transform.scale(whiteQueen, (75, 75))
blackPawn = pygame.image.load('images/Chess/128px/b_pawn_png_shadow_128px.png')
blackPawn = pygame.transform.scale(blackPawn, (75, 75))
blackRook = pygame.image.load('images/Chess/128px/b_rook_png_shadow_128px.png')
blackRook = pygame.transform.scale(blackRook, (75, 75))
blackBishop = pygame.image.load('images/Chess/128px/b_bishop_png_shadow_128px.png')
blackBishop = pygame.transform.scale(blackBishop, (75, 75))
blackKnight = pygame.image.load('images/Chess/128px/b_knight_png_shadow_128px.png')
blackKnight = pygame.transform.scale(blackKnight, (75, 75))
blackKing = pygame.image.load('images/Chess/128px/b_king_png_shadow_128px.png')
blackKing = pygame.transform.scale(blackKing, (75, 75))
blackQueen = pygame.image.load('images/Chess/128px/b_queen_png_shadow_128px.png')
blackQueen = pygame.transform.scale(blackQueen, (75, 75))
highlight_block = pygame.image.load('images/Chess/128px/highlight_128px.png')
highlight_block = pygame.transform.scale(highlight_block, (75, 75))
screen = None
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 20)

def initialize():
    """
    Initializes the Pygame module, sets up the game window, and loads the images for the chess pieces and board.
    """
    global screen
    pygame.init()
    pygame.display.set_caption('Chess game')
    icon = pygame.image.load('images/icon.png')
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode((600, 650))
    screen.fill((0, 0, 0))

def draw_background(board):
    """
    Draws the chess board and pieces on the Pygame window based on the current state of the board.
    The function uses the screen.blit method to draw the images for the chess pieces on the board.
    """
    block_x = 0
    for i in range(4):
        block_y = 0
        for j in range(4):
            screen.blit(light_block, (block_x, block_y))
            screen.blit(dark_block, (block_x + 75, block_y))
            screen.blit(light_block, (block_x + 75, block_y + 75))
            screen.blit(dark_block, (block_x, block_y + 75))
            block_y += 150
        block_x += 150
    step_x = 0
    step_y = pygame.display.get_surface().get_size()[0] - 75
    for i in range(8):
        for j in range(8):
            if isinstance(board[i][j], ChessPiece):
                obj = globals()[f'{board[i][j].color}{board[i][j].type}']
                screen.blit(obj, (step_x, step_y))
            step_x += 75
        step_x = 0
        step_y -= 75
    pygame.display.update()

def white_win_text(text):
    """
    Displays a message on the screen and prompts the user to restart the game by pressing the "SPACE" key when the game is over and white wins.
    """
    if 'White Win' in text:
        x = 230
    else:
        x = 200
    s = pygame.Surface((400, 50))
    s.fill((0, 0, 0))
    screen.blit(s, (100, 600))
    text_surface = font.render(text, False, (237, 237, 237))
    text_surface_restart = font.render('PRESS "SPACE" TO RESTART', False, (237, 237, 237))
    screen.blit(text_surface, (x, 600))
    screen.blit(text_surface_restart, (150, 620))
    pygame.display.update()

def black_win_text(text):
    """
    Displays a message on the screen and prompts the user to restart the game by pressing the "SPACE" key when the game is over and black wins.
    """
    if 'Black Win' in text:
        x = 230
    else:
        x = 200
    s = pygame.Surface((400, 50))
    s.fill((0, 0, 0))
    screen.blit(s, (100, 600))
    text_surface = font.render(text, False, (237, 237, 237))
    text_surface_restart = font.render('PRESSSPACE" TO RESTART', False, (237, 237, 237))
    screen.blit(text_surface, (x, 600))
    screen.blit(text_surface_restart, (150, 620))
    pygame.display.update()


def start(board):
    # Initialize variables
    global screen
    possible_piece_moves = []
    running = True
    visible_moves = False
    dimensions = pygame.display.get_surface().get_size()
    game_over_white_win = False
    game_over_black_win = False
    piece = None

    # If game mode is 1 and AI is enabled, get AI move and draw background
    if board.game_mode == 1 and board.ai:
        get_ai_move(board)
        draw_background(board)

    # Main game loop
    while running:
        # Check if game over and display appropriate text
        if game_over_black_win:
            black_win_text(game_over_black_win_txt)
        if game_over_white_win:
            white_win_text(game_over_white_win_txt)

        # Handle events
        for event in pygame.event.get():
            # Quit event
            if event.type == pygame.QUIT:
                running = False

            # Space key event to restart game after game over
            if (game_over_white_win or game_over_black_win) and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True

            # Mouse button down event to select piece and move
            if event.type == pygame.MOUSEBUTTONDOWN and (not game_over_black_win) and (not game_over_white_win):
                # Get x and y coordinates of mouse click
                x = 7 - pygame.mouse.get_pos()[1] // 75
                y = pygame.mouse.get_pos()[0] // 75

                # Check if selected piece is valid and get possible moves
                if isinstance(board[x][y], ChessPiece) and (
                        board.get_player_color() == board[x][y].color or not board.ai) and (
                        x, y) not in possible_piece_moves:
                    piece = board[x][y]
                    moves = piece.filter_moves(piece.get_moves(board), board)
                    move_positions = []
                    possible_piece_moves = []

                    # Get move positions and possible piece moves
                    for move in moves:
                        move_positions.append((dimensions[0] - (8 - move[1]) * 75, dimensions[1] - move[0] * 75 - 125))
                        move_x = 7 - move_positions[-1][1] // 75
                        move_y = move_positions[-1][0] // 75
                        possible_piece_moves.append((move_x, move_y))

                    # Draw possible moves
                    if visible_moves:
                        draw_background(board)
                        visible_moves = False
                    for move in move_positions:
                        visible_moves = True
                        screen.blit(highlight_block, (move[0], move[1]))
                        pygame.display.update()

                # If move is valid, make move and check for game over
                else:
                    clicked_move = (x, y)
                    try:
                        if clicked_move in possible_piece_moves:
                            board.make_move(piece, x, y)
                            possible_piece_moves.clear()
                            draw_background(board)
                            if board.ai:
                                get_ai_move(board)
                                draw_background(board)
                        if board.black_won():
                            game_over_black_win = True
                            game_over_black_win_txt = 'Black Win!'
                        if board.white_won():
                            game_over_white_win = True
                            game_over_white_win_txt = 'White Win!'
                    except UnboundLocalError:
                        pass
