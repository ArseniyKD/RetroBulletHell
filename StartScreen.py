import pygame
import sys
import os
import shared
import time
from text_to_screen import text_to_screen

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((shared.width, shared.height))
screen.fill(shared.BLACK)
backdropbox = screen.get_rect()

# the background image came from here:
# https://pxhere.com/en/photo/610854
def StartScreenSequence():
    BGimage = pygame.image.load(os.path.join('images','menuBG.png')).convert()
    screen.blit(BGimage, (0,0))

    startTime = pygame.time.get_ticks()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return False
            elif event.type == pygame.KEYDOWN:
                return False

        curTime = pygame.time.get_ticks() - startTime
        if curTime >= 3500:
            text_to_screen(screen, "or the exit button", 195, shared.height - 30, 14, shared.WHITE)
        elif curTime >= 3000:
            text_to_screen(screen, "just not the power button", 170, shared.height - 50, 15, shared.WHITE)
        elif curTime >= 2250:
            text_to_screen(screen, "PRESS ANY BUTTON TO CONTINUE", 40, shared.height - 100, 30, shared.WHITE)
        elif curTime >= 1500:
            text_to_screen(screen, "HELL", shared.width - 345, shared.height / 3 + 75,  100, shared.RED)
        elif curTime >= 750:
            text_to_screen(screen, "BULLET", shared.width - 405, shared.height / 3, 100, shared.BLUE)
        else:
            text_to_screen(screen, "RETRO", shared.width - 385, shared.height / 3 - 75, 100, shared.GOLD)

        pygame.display.flip()  # required to show changes to screen
        shared.clock.tick(shared.fps) # limit fps of game to shared.fps
