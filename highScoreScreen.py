import pygame
import sys
import os
import shared
import time
import HighScoreTracking
from text_to_screen import text_to_screen

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((shared.width, shared.height))
screen.fill(shared.BLACK)
backdropbox = screen.get_rect()

buttonBox = pygame.Rect(75, 595, 345, 85)


# the background image came from here:
# https://pxhere.com/en/photo/610854
def drawHighScoreScreen():
    BGimage = pygame.image.load(os.path.join('images','menuBG.png')).convert()
    screen.blit(BGimage, (0,0))

    text_to_screen(screen, "HIGH   SCORES", 40, 20, 75, shared.GOLD)
    pygame.draw.line(screen, shared.WHITE, (0, 80), (shared.width, 80), 2)
    pygame.draw.line(screen, shared.GRAY, (55, 105), (55, 555), 2)
    pygame.draw.line(screen, shared.GRAY, (285, 105), (285, 555), 2)
    text_to_screen(screen, "NAME", 60, 90, 75, shared.GOLD)
    text_to_screen(screen, "SCORE", 290, 90, 75, shared.GOLD)
    pygame.draw.line(screen, shared.GRAY, (0, 155), (shared.width, 155), 2)
    text_to_screen(screen, "1", 10, 110 + 40, 50, shared.GOLD)
    pygame.draw.line(screen, shared.GRAY, (0, 195), (shared.width, 195), 2)
    text_to_screen(screen, "2", 10, 150 + 40, 50, shared.GOLD)
    pygame.draw.line(screen, shared.GRAY, (0, 235), (shared.width, 235), 2)
    text_to_screen(screen, "3", 10, 190 + 40, 50, shared.GOLD)
    pygame.draw.line(screen, shared.GRAY, (0, 275), (shared.width, 275), 2)
    text_to_screen(screen, "4", 10, 230 + 40, 50, shared.GOLD)
    pygame.draw.line(screen, shared.GRAY, (0, 315), (shared.width, 315), 2)
    text_to_screen(screen, "5", 10, 270 + 40, 50, shared.GOLD)
    pygame.draw.line(screen, shared.GRAY, (0, 355), (shared.width, 355), 2)
    text_to_screen(screen, "6", 10, 310 + 40, 50, shared.GOLD)
    pygame.draw.line(screen, shared.GRAY, (0, 395), (shared.width, 395), 2)
    text_to_screen(screen, "7", 10, 350 + 40, 50, shared.GOLD)
    pygame.draw.line(screen, shared.GRAY, (0, 435), (shared.width, 435), 2)
    text_to_screen(screen, "8", 10, 390 + 40, 50, shared.GOLD)
    pygame.draw.line(screen, shared.GRAY, (0, 475), (shared.width, 475), 2)
    text_to_screen(screen, "9", 10, 430 + 40, 50, shared.GOLD)
    pygame.draw.line(screen, shared.GRAY, (0, 515), (shared.width, 515), 2)
    text_to_screen(screen, "10", 8, 470 + 42, 40, shared.GOLD)
    pygame.draw.line(screen, shared.GRAY, (0, 555), (shared.width, 555), 2)
    pygame.draw.rect(screen, shared.WHITE, buttonBox, 2)
    text_to_screen(screen, "MAIN MENU", 80, 600, 75, shared.GOLD)


def drawHighScores():
    count = 0
    highScores = HighScoreTracking.HighScore()
    allScores = highScores.getAllHighScores()
    for score in allScores:
        name = ''
        for c in score[1]:
            if c == '_':
                name += '   '
            else:
                name += c
        scoreVal = ''
        originalVal = str(score[0])
        for c in originalVal:
            if c == '-':
                scoreVal += 'N'
            else:
                scoreVal += c
        text_to_screen(screen, name, 60, 157 + count*40, 35, shared.WHITE)
        text_to_screen(screen, scoreVal, 290, 150 + count*40, 50, shared.WHITE)
        count += 1

def sequence():
    quit = False
    exit = False
    initHighScoreScreen = True
    while not exit:
        if initHighScoreScreen:
            drawHighScoreScreen()
            drawHighScores()
            initHighScoreScreen = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
                quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    exit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttonBox.collidepoint(event.pos):
                    exit = True
    if quit:
        pygame.quit()
        sys.exit()
