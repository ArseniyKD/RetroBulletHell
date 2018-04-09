import pygame
import sys
import os
import shared
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (249, 166, 2)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

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

# the background image came from here:
# https://pxhere.com/en/photo/610854
def StartScreenSequence():
    BGimage = pygame.image.load(os.path.join('images','menuBG.png')).convert()
    screen.blit(BGimage, (0,0))
    text_to_screen(screen, "RETRO", shared.width - 385, shared.height / 3 - 75, 100, GOLD)
    time.sleep(0.5)
    text_to_screen(screen, "BULLET", shared.width - 405, shared.height / 3, 100, BLUE)
    time.sleep(0.5)
    text_to_screen(screen, "HELL", shared.width - 345, shared.height / 3 + 75,  100, RED)
    time.sleep(0.50)
    text_to_screen(screen, "PRESS ANY BUTTON TO CONTINUE", 40, shared.height - 100, 30, WHITE)
    time.sleep(0.5)
    text_to_screen(screen, "just not the power button", 170, shared.height - 50, 15, WHITE)

def sequence():
    drawStartScreenSequence = True
    while True:
        if drawStartScreenSequence:
            StartScreenSequence()
            drawStartScreenSequence = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return False
            elif event.type == pygame.KEYDOWN:
                return False
