import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Define the colors
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Define the button
button_color = (0, 255, 0)  # Green
button_pos = (WIDTH // 2 - 50, HEIGHT // 2 - 20)
button_size = (100, 40)
button = pygame.Rect(button_pos, button_size)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE')
screen.fill((28, 170, 156))

# Define the scores
score_X = 0
score_O = 0
# Board
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Pygame window
def draw_scores():
    font = pygame.font.Font(None, 24)
    score_text = font.render('Score: X = ' + str(score_X) + ', O = ' + str(score_O), True, (0, 0, 0))
    screen.blit(score_text, (15, 15))

def draw_button():
    pygame.draw.rect(screen, button_color, button)
    font = pygame.font.Font(None, 24)
    text = font.render('Restart', True, (0, 0, 0))
    text_rect = text.get_rect(center=button.center)
    screen.blit(text, text_rect)

def draw_lines():
    # 1st horizontal
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    # 2nd horizontal
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)

    # 1st vertical
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    # 2nd vertical
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] is None

def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                return False
    return True

def draw_vertical_winning_line(col, player):
    posX = col * SQUARE_SIZE + SQUARE_SIZE//2
    if player == 'X':
        color = CROSS_COLOR
    else: 
        color = CIRCLE_COLOR
    pygame.draw.line(screen, color, (posX, 15), (posX, HEIGHT - 15), LINE_WIDTH)

def draw_horizontal_winning_line(row, player):
    posY = row * SQUARE_SIZE + SQUARE_SIZE//2
    if player == 'X':
        color = CROSS_COLOR
    else: 
        color = CIRCLE_COLOR
    pygame.draw.line(screen, color, (15, posY), (WIDTH - 15, posY), LINE_WIDTH)

def draw_asc_diagonal(player):
    if player == 'X':
        color = CROSS_COLOR
    else: 
        color = CIRCLE_COLOR
    pygame.draw.line(screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), WIN_LINE_WIDTH)

def draw_desc_diagonal(player):
    if player == 'X':
        color = CROSS_COLOR
    else: 
        color = CIRCLE_COLOR
    pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), WIN_LINE_WIDTH)


def check_win(player):
    global score_X, score_O
    # vertical win check
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_winning_line(col, player)
            if player == 'X':
                score_X += 1
            else:
                score_O += 1
            return True
    # horizontal win check
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_winning_line(row, player)
            if player == 'X':
                score_X += 1
            else:
                score_O += 1
            return True
    # asc diagonal win check
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_asc_diagonal(player)
        if player == 'X':
            score_X += 1
        else:
            score_O += 1
        return True
    # desc diagonal win check
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_desc_diagonal(player)
        if player == 'X':
            score_X += 1
        else:
            score_O += 1
        return True
    return False


def check_tie():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                return False
    return True


def restart():
    screen.fill((28, 170, 156))
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = None

draw_lines()

# Mainloop
player = 'X'
game_over = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] # x
            mouseY = event.pos[1] # y
            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE
            if available_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)
                if check_win(player):
                    game_over = True
                    draw_button()  # Draw the button when the game is over
                elif check_tie():
                    game_over = True
                    draw_button()  # Draw the button when the game is a tie
                player = 'O' if player == 'X' else 'X'
                draw_figures()
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:  # Check for clicks when the game is over
            if button.collidepoint(event.pos):  # Check if the click is on the button
                restart()
                player = 'X'
                game_over = False
    draw_scores()
    pygame.display.update()
    time.sleep(0.3)  # added delay for better visualization
