import gameUtil as u
import pygame
import sys
import math

global screen
global width
global height


def setScreen():
    global screen
    global width
    global height
    pygame.init()
    width = u.COLUMN_COUNT * u.SQUARESIZE
    height = (u.ROW_COUNT+1) * u.SQUARESIZE

    size = (width, height)
    screen = pygame.display.set_mode(size)

def eventListener(turn):
    global screen
    global width
    global height
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("exit")
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, u.BLACK, (0, 0, width, u.SQUARESIZE))
            posx = event.pos[0]
            if turn == u.PLAYER:
                pygame.draw.circle(screen, u.RED, (posx, int(u.SQUARESIZE / 2)), u.RADIUS)
            else:
                pygame.draw.circle(screen, u.YELLOW, (posx, int(u.SQUARESIZE / 2)), u.RADIUS)
            pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, u.BLACK, (0, 0, width, u.SQUARESIZE))
            print(event.pos)
            posx = event.pos[0]
            col = int(math.floor(posx / u.SQUARESIZE))
            return col

def winning(piece, color):
    myfont = pygame.font.SysFont("monospace", 75)
    lable = myfont.render("Player "+str(piece)+" wins!", 1, color)
    screen.blit(lable, (40, 10))

def wait_to_end():
    pygame.time.wait(3000)

def draw_board(board):
    for c in range (u.COLUMN_COUNT):
        for r in range (u.ROW_COUNT):
            pygame.draw.rect(screen, u.BLUE, (c*u.SQUARESIZE, r*u.SQUARESIZE+u.SQUARESIZE, u.SQUARESIZE,u.SQUARESIZE))
            pygame.draw.circle(screen, u.BLACK,
                               (int(c*u.SQUARESIZE+u.SQUARESIZE/2),
                                int(r*u.SQUARESIZE+u.SQUARESIZE+u.SQUARESIZE/2)),u.RADIUS )
    for c in range(u.COLUMN_COUNT):
        for r in range(u.ROW_COUNT):
            if (board[r][c] == u.PLAYER_PIECE):
                pygame.draw.circle(screen, u.RED, (
                                    int(c * u.SQUARESIZE + u.SQUARESIZE / 2),
                                    height - int(r * u.SQUARESIZE + u.SQUARESIZE / 2)), u.RADIUS)
            if (board[r][c] == u.AI_PIECE):
                pygame.draw.circle(screen, u.YELLOW,
                                   (int(c * u.SQUARESIZE + u.SQUARESIZE / 2),
                                    height-int(r * u.SQUARESIZE + u.SQUARESIZE / 2)),
                                    u.RADIUS)

    pygame.display.update()

