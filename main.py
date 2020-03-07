import pygame
import math
pygame.init()

fps = 30
screen_width = 600
screen_height = 600
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Checkers")
clock = pygame.time.Clock()


x = 200
y = 500
width = 40
vel = 10

isJump = False
jumpCount = 10


def getCenterPosForBoardSquare():
    cx = 0
    cy = 0

    return (cx, cy)


def redrawGameWindow():
    #Board
    win.fill((247, 126, 0))
    b1 = win.blit(pygame.image.load('images/board.png'), (50, 50))

    win.blit(pygame.image.load('images/sort.png'), (x - 23, y - 23))
    #pygame.draw.circle(win, (255, 0, 0), (x + 65, y + 10), width)

    pygame.display.update()

drag = False
run = True
# Main loop
while run:
    # fps
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Man skal faktisk trække i tingen
            if abs(x - pygame.mouse.get_pos()[0]) < 25 and abs(y - pygame.mouse.get_pos()[1]) < 25:
                drag = True
        if event.type == pygame.MOUSEBUTTONUP:
            drag = False
        if event.type == pygame.MOUSEMOTION:
            if drag:
                (x, y) = pygame.mouse.get_pos()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x > vel:
        x -= vel
    if keys[pygame.K_RIGHT] and x < screen_width - width:
        x += vel
    if not isJump:
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCount >= - 10:
            neg = 1
            if jumpCount < 0:
                neg = -1
            y -= (jumpCount ** 2) // 2 * neg
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10
    redrawGameWindow()


pygame.quit()

