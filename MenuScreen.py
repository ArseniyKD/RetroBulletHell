import pygame
import sys
import os
import shared
import time

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((shared.width, shared.height))
screen.fill(shared.BLACK)
backdropbox = screen.get_rect()

newGameBox = pygame.Rect(100, 105, 315, 85)
continueGameBox = pygame.Rect(10, 205, 490, 80)
lowDiffBox = pygame.Rect(40, 385, 100, 60)
medDiffBox = pygame.Rect(155, 385, 180, 60)
hiDiffBox = pygame.Rect(340, 385, 130, 60)
highScoresBox = pygame.Rect(30, 460, 435, 85)
quitBox = pygame.Rect(150, 580, 175, 85)

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
def drawMenuScreen():
    BGimage = pygame.image.load(os.path.join('images','menuBG.png')).convert()
    screen.blit(BGimage, (0,0))
    text_to_screen(screen, "RETRO", 30, 20, 50, shared.GOLD)
    text_to_screen(screen, "BULLET", 190, 20, 50, shared.BLUE)
    text_to_screen(screen, "HELL", 370, 20, 50, shared.RED)
    pygame.draw.line(screen, shared.WHITE, (0, 80), (shared.width, 80), 2)
    text_to_screen(screen, "NEW GAME", 110, 50 + 60, 75, shared.GOLD)
    pygame.draw.rect(screen, shared.GRAY, newGameBox, 3)
    text_to_screen(screen, "CONTINUE GAME", 15, 150 + 60, 70, shared.GOLD)
    pygame.draw.rect(screen, shared.GRAY, continueGameBox, 3)
    text_to_screen(screen, "DIFFICULTY", 50, 250 + 60, 75, shared.GOLD)
    chooseDifficulty(shared.difficulty)
    pygame.draw.rect(screen, shared.GRAY, lowDiffBox, 3)
    pygame.draw.rect(screen, shared.GRAY, medDiffBox, 3)
    pygame.draw.rect(screen, shared.GRAY, hiDiffBox, 3)
    text_to_screen(screen, "HIGH SCORES", 40, 410 + 60, 75, shared.GOLD)
    pygame.draw.rect(screen, shared.GRAY, highScoresBox, 3)
    text_to_screen(screen, "QUIT", 160, 530 + 60, 75, shared.GOLD)
    pygame.draw.rect(screen, shared.GRAY, quitBox, 3)
    pygame.display.update()

def chooseDifficulty(diffLevel):
    if diffLevel == 0.5:
        text_to_screen(screen, "LOW", 50, 330 + 60, 50, shared.WHITE)
        text_to_screen(screen, "MEDIUM", 160, 330 + 60, 50, shared.GOLD)
        text_to_screen(screen, "HIGH", 350, 330 + 60, 50, shared.GOLD)
    if diffLevel == 1:
        text_to_screen(screen, "LOW", 50, 330 + 60, 50, shared.GOLD)
        text_to_screen(screen, "MEDIUM", 160, 330 + 60, 50, shared.WHITE)
        text_to_screen(screen, "HIGH", 350, 330 + 60, 50, shared.GOLD)
    if diffLevel == 1.5:
        text_to_screen(screen, "LOW", 50, 330 + 60, 50, shared.GOLD)
        text_to_screen(screen, "MEDIUM", 160, 330 + 60, 50, shared.GOLD)
        text_to_screen(screen, "HIGH", 350, 330 + 60, 50, shared.WHITE)


def processEvents(event):
    # Time to start a new game
    if  newGameBox.collidepoint(event.pos):
        return 2
    # Load an existing game or not do anything if no save file
    if continueGameBox.collidepoint(event.pos):
        return 4
    # Low difficulty selected
    if lowDiffBox.collidepoint(event.pos):
        chooseDifficulty(0.5)
        shared.difficulty = 0.5
        return 0
    # medium difficulty selected
    if medDiffBox.collidepoint(event.pos):
        chooseDifficulty(1)
        shared.difficulty = 1
        return 0
    # high difficuly selected
    if hiDiffBox.collidepoint(event.pos):
        chooseDifficulty(1.5)
        shared.difficulty = 1.5
        return 0
    # open the high scores screen
    if highScoresBox.collidepoint(event.pos):
        return 3
    # quit the game from the quit button in the menu
    if quitBox.collidepoint(event.pos):
        return 1

def sequence():
    exit = False
    quit = False
    initMenuScreen = True
    toStart = False
    toHighScore = False
    while not exit:
        if initMenuScreen:
            drawMenuScreen()
            initMenuScreen = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
                quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                exit = processEvents(event)

    if exit == 1 or quit:
        pygame.quit()
        sys.exit()

    if exit == 2:
        return 1
    if exit == 3:
        return 0
    if exit == 4:
        return 2
