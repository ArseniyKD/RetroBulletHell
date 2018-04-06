import pygame
import sys
import os
import shared
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (249, 166, 2)

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((shared.width, shared.height))
screen.fill(BLACK)
backdropbox = screen.get_rect()

def text_to_screen(screen, text, x, y, size = 50,
            color = (200, 000, 000), font_type = 'images/fonts/ARCADECLASSIC.TTF'):
    try:
        text = str(text)
        font = pygame.font.Font(font_type, size)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))
        pygame.display.update()

    except Exception:
        print('Font Error, saw it coming')


def gameOverSequence():
    text_to_screen(screen, 'GAME OVER', shared.width / 5 - 25, shared.height / 5, 75, GOLD)
    time.sleep(1)
    screen.fill(BLACK)
    pygame.display.update()
    time.sleep(0.25)
    text_to_screen(screen, "GAME OVER", shared.width / 5 - 25, shared.height / 5, 75, GOLD)
    time.sleep(1)
    screen.fill(BLACK)
    pygame.display.update()
    time.sleep(0.25)
    text_to_screen(screen, "GAME OVER", shared.width / 5 - 25, shared.height / 5, 75, GOLD)
    text_to_screen(screen, 'YOUR SCORE IS  {0}'.format(15000), shared.width / 10 - 30, shared.height / 3, 50, GOLD)

exit = False
drawGameOverSequence = True
while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
            break

    if drawGameOverSequence:
        gameOverSequence()
        drawGameOverSequence = False

pygame.quit()
sys.exit()
