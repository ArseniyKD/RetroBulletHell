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
    text_to_screen(screen, 'ENTER  NAME', 25, 400, 40, GOLD)
    text_to_screen(screen, 'CONTINUE', 85,  500, 75, GOLD)
    pygame.draw.rect(screen, WHITE, continue_box, 3)



exit = False
drawGameOverSequence = True
name = ''
input_box = pygame.Rect(shared.width / 2, 400, 250, 40)
continue_box = pygame.Rect(75, 495, 345, 85)
while not exit:
    if drawGameOverSequence:
        gameOverSequence()
        drawGameOverSequence = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                name = name[:-1]
            elif event.key == pygame.K_RETURN:
                continue
            else:
                if len(name) < 11:
                    name += event.unicode

    pygame.draw.rect(screen, BLACK, input_box)
    text_to_screen(screen, name, input_box.x, input_box.y, 40, GOLD)


pygame.quit()
sys.exit()
