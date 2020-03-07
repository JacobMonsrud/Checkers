import pygame

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


def getCenterPosForBoardSquare(xpos: int, ypos: int):
    indexX = 0
    indexY = 0


    jumpX = screen_width // 10
    jumpY = screen_height // 10

    for i in range(1, 9):
        xleft = i * jumpX
        if xleft <= xpos <= xleft + jumpX:
            indexX = i

        yleft = i * jumpY
        if yleft <= ypos <= yleft + jumpY:
            indexY = i

    centerX = (indexX * jumpX) + (jumpX // 2)
    centerY = (indexY* jumpY) + (jumpY // 2)

    return (centerX, centerY)


def redrawGameWindow():
    # Board
    win.fill((247, 126, 0))
    win.blit(pygame.image.load('images/board.png'), (50, 50))

    win.blit(pygame.image.load('images/sort.png'), (x - 23, y - 23))
    # pygame.draw.circle(win, (255, 0, 0), (x + 65, y + 10), width)

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
            (x, y) = getCenterPosForBoardSquare(x, y)
            drag = False
        if event.type == pygame.MOUSEMOTION:
            if drag:
                (x, y) = pygame.mouse.get_pos()

    redrawGameWindow()


pygame.quit()

