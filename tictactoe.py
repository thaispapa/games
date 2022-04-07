import pygame
import sys
import numpy as np

pygame.init()

WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55
BG_COLOR = (93, 173, 218)
LINE_COLOR = (93, 159, 208)
CIRCLE_COLOR = (255, 255, 255)
CROSS_COLOR = (71, 71, 71)
B_ROWS = 3
B_COLUMNS = 3

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE')
screen.fill(BG_COLOR)

board = np.zeros((B_ROWS, B_COLUMNS))
print(board)


def draw_lines():
    pygame.draw.line(screen, LINE_COLOR, (0, 200), (600, 200), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 400), (600, 400), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (200, 0), (200, 600), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (400, 0), (400, 600), LINE_WIDTH)


def draw_figures():
    for row in range(B_ROWS):
        for column in range(B_COLUMNS):
            if board[row][column] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(column * 200 + 200 / 2),
                                                          int(row * 200 + 200 / 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][column] == 2:
                pygame.draw.line(screen, CROSS_COLOR, (column * 200 + SPACE, row * 200 + 200 - SPACE),
                                 (column * 200 + 200 - SPACE, row * 200 + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (column * 200 + SPACE, row * 200 + SPACE),
                                 (column * 200 + 200 - SPACE, row * 200 + 200 - SPACE), CROSS_WIDTH)


def mark_square(row, column, player):
    board[row][column] = player


def available_square(row, column):
    return board[row][column] == 0


def is_board_full():
    for row in range(B_ROWS):
        for column in range(B_COLUMNS):
            if board[row][column] == 0:
                return False

    return True


def check_win(player):
    # vertical win check
    for column in range(B_COLUMNS):
        if board[0][column] == player and  board[1][column] == player and board[2][column] == player:
            draw_vertical_winning_line(column, player)
            return True

    # horizontal win check
    for row in range(B_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_winning_line(row, player)
            return True

    # asc diagonal win check
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_asc_diagonal(player)
        return True

    # desc diagonal win check
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_desc_diagonal(player)
        return True

    return False


def draw_vertical_winning_line(column, player):
    global color
    posX = column * 200 + 100

    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line(screen, color, (posX, 15), (posX, HEIGHT - 15), 15)


def draw_horizontal_winning_line(row, player):
    global color
    posY = row * 200 + 100

    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line(screen, color, (15, posY), (WIDTH - 15, posY), 15)


def draw_asc_diagonal(player):
    global color
    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line(screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), 15)


def draw_desc_diagonal(player):
    global color
    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), 15)


def restart():
    screen.fill(BG_COLOR)
    draw_lines()
    player = 1
    for row in range(B_ROWS):
        for column in range(B_COLUMNS):
            board[row][column] = 0


draw_lines()

player = 1
game_over = False

# mainloop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]  # x
            mouseY = event.pos[1]  # y

            clicked_row = int(mouseY // 200)
            clicked_column = int(mouseX // 200)

            if available_square(clicked_row, clicked_column):
                if player == 1:
                    mark_square(clicked_row, clicked_column, 1)
                    if check_win(player):
                        game_over = True
                    player = 2
                elif player == 2:
                    mark_square(clicked_row, clicked_column, 2)
                    if check_win(player):
                        game_over = True
                    player = 1
                draw_figures()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                game_over = False

    pygame.display.update()
