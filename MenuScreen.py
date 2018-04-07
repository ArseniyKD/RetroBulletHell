import pygame
import sys
import os
import shared
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (249, 166, 2)
BLUE = (0, 0, 255)
GRAY = (134, 136, 138)
RED = (255, 0, 0)

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((shared.width, shared.height))
screen.fill(BLACK)
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

def drawMenuScreen():
    text_to_screen(screen, "RETRO", 30, 20, 50, GOLD)
    text_to_screen(screen, "BULLET", 190, 20, 50, BLUE)
    text_to_screen(screen, "HELL", 370, 20, 50, RED)
    pygame.draw.line(screen, WHITE, (0, 80), (shared.width, 80), 2)
    text_to_screen(screen, "NEW GAME", 110, 50 + 60, 75, GOLD)
    pygame.draw.rect(screen, GRAY, newGameBox, 3)
    text_to_screen(screen, "CONTINUE GAME", 15, 150 + 60, 70, GOLD)
    pygame.draw.rect(screen, GRAY, continueGameBox, 3)
    text_to_screen(screen, "DIFFICULTY", 50, 250 + 60, 75, GOLD)
    text_to_screen(screen, "LOW", 50, 330 + 60, 50, GOLD)
    pygame.draw.rect(screen, GRAY, lowDiffBox, 3)
    text_to_screen(screen, "MEDIUM", 160, 330 + 60, 50, WHITE)
    pygame.draw.rect(screen, GRAY, medDiffBox, 3)
    text_to_screen(screen, "HIGH", 350, 330 + 60, 50, GOLD)
    pygame.draw.rect(screen, GRAY, hiDiffBox, 3)
    text_to_screen(screen, "HIGH SCORES", 40, 410 + 60, 75, GOLD)
    pygame.draw.rect(screen, GRAY, highScoresBox, 3)
    text_to_screen(screen, "QUIT", 160, 530 + 60, 75, GOLD)
    pygame.draw.rect(screen, GRAY, quitBox, 3)
    pygame.display.update()

def chooseDifficulty(diffLevel):
    if diffLevel == 0:
        text_to_screen(screen, "LOW", 50, 330 + 60, 50, WHITE)
        text_to_screen(screen, "MEDIUM", 160, 330 + 60, 50, GOLD)
        text_to_screen(screen, "HIGH", 350, 330 + 60, 50, GOLD)
    if diffLevel == 1:
        text_to_screen(screen, "LOW", 50, 330 + 60, 50, GOLD)
        text_to_screen(screen, "MEDIUM", 160, 330 + 60, 50, WHITE)
        text_to_screen(screen, "HIGH", 350, 330 + 60, 50, GOLD)
    if diffLevel == 2:
        text_to_screen(screen, "LOW", 50, 330 + 60, 50, GOLD)
        text_to_screen(screen, "MEDIUM", 160, 330 + 60, 50, GOLD)
        text_to_screen(screen, "HIGH", 350, 330 + 60, 50, WHITE)


def processEvents(event):
    if  newGameBox.collidepoint(event.pos):
        print("Time to start a new game")
        return False
    if continueGameBox.collidepoint(event.pos):
        print("Load an existing game or not do anything if no save file")
        return False
    if lowDiffBox.collidepoint(event.pos):
        print("Low difficulty selected")
        chooseDifficulty(0)
        return False
    if medDiffBox.collidepoint(event.pos):
        print("medium difficulty selected")
        chooseDifficulty(1)
        return False
    if hiDiffBox.collidepoint(event.pos):
        print("high difficuly selected")
        chooseDifficulty(2)
        return False
    if highScoresBox.collidepoint(event.pos):
        print("open the high scores screen")
        return False
    if quitBox.collidepoint(event.pos):
        print("quit the game from the quit button in the menu")
        return True

exit = False
initMenuScreen = True

while not exit:
    if initMenuScreen:
        drawMenuScreen()
        initMenuScreen = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            exit = processEvents(event)


print("Off to do better things")
pygame.quit()
sys.exit()
