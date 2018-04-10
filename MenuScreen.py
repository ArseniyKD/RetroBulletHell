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

# the background image came from here:
# https://pxhere.com/en/photo/610854
def drawMenuScreen():
    BGimage = pygame.image.load(os.path.join('images','menuBG.png')).convert()
    screen.blit(BGimage, (0,0))

    text_to_screen(screen, "RETRO", 30, 20, 50, GOLD)
    text_to_screen(screen, "BULLET", 190, 20, 50, BLUE)
    text_to_screen(screen, "HELL", 370, 20, 50, RED)

    pygame.draw.line(screen, WHITE, (0, 80), (shared.width, 80), 2)
    text_to_screen(screen, "NEW GAME", 110, 50 + 60, 75, WHITE)
    pygame.draw.rect(screen, WHITE, newGameBox, 3)
    canLoad = False
    try:
        istream = open('save.txt', 'r').close()
        canLoad = True
    except:
        text_to_screen(screen, "CONTINUE GAME", 15, 150 + 60, 70, GRAY)
    if canLoad:
        text_to_screen(screen, "CONTINUE GAME", 15, 150 + 60, 70, GOLD)

    pygame.draw.rect(screen, GRAY, continueGameBox, 3)
    text_to_screen(screen, "DIFFICULTY", 50, 250 + 60, 75, GOLD)
    chooseDifficulty(shared.difficulty)
    pygame.draw.rect(screen, GRAY, lowDiffBox, 3)
    pygame.draw.rect(screen, GRAY, medDiffBox, 3)
    pygame.draw.rect(screen, GRAY, hiDiffBox, 3)
    text_to_screen(screen, "HIGH SCORES", 40, 410 + 60, 75, GOLD)
    pygame.draw.rect(screen, GRAY, highScoresBox, 3)
    text_to_screen(screen, "QUIT", 160, 530 + 60, 75, GOLD)
    pygame.draw.rect(screen, GRAY, quitBox, 3)
    pygame.display.update()

    return canLoad

def colourBox(curr, colour, diffLevel = shared.difficulty):
    if curr == 0:
        pygame.draw.rect(screen, colour, newGameBox, 3)
    elif curr == 1:
        pygame.draw.rect(screen, colour, continueGameBox, 3)
    elif curr == 2:
        if diffLevel == 0.5:
            pygame.draw.rect(screen, colour, lowDiffBox, 3)
        elif diffLevel == 1:
            pygame.draw.rect(screen, colour, medDiffBox, 3)
        elif diffLevel == 1.5:
            pygame.draw.rect(screen, colour, hiDiffBox, 3)
    elif curr == 3:
        pygame.draw.rect(screen, colour, highScoresBox, 3)
    elif curr == 4:
        pygame.draw.rect(screen, colour, quitBox, 3)

def chooseDifficulty(diffLevel):
    if diffLevel == 0.5:
        text_to_screen(screen, "LOW", 50, 330 + 60, 50, WHITE)
        text_to_screen(screen, "MEDIUM", 160, 330 + 60, 50, GOLD)
        text_to_screen(screen, "HIGH", 350, 330 + 60, 50, GOLD)
    if diffLevel == 1:
        text_to_screen(screen, "LOW", 50, 330 + 60, 50, GOLD)
        text_to_screen(screen, "MEDIUM", 160, 330 + 60, 50, WHITE)
        text_to_screen(screen, "HIGH", 350, 330 + 60, 50, GOLD)
    if diffLevel == 1.5:
        text_to_screen(screen, "LOW", 50, 330 + 60, 50, GOLD)
        text_to_screen(screen, "MEDIUM", 160, 330 + 60, 50, GOLD)
        text_to_screen(screen, "HIGH", 350, 330 + 60, 50, WHITE)

def redrawButton(prev, curr):
    if prev != curr:
        buttonStrings = {0:("NEW GAME", 110, 50 + 60, 75), 1:("CONTINUE GAME", 15, 150 + 60, 70), 2:("DIFFICULTY", 50, 250 + 60, 75), 3:("HIGH SCORES", 40, 410 + 60, 75), 4: ("QUIT", 160, 530 + 60, 75)}
        text_to_screen(screen, buttonStrings[prev][0], buttonStrings[prev][1], buttonStrings[prev][2], buttonStrings[prev][3], GOLD)
        if curr != 2:
            text_to_screen(screen, buttonStrings[curr][0], buttonStrings[curr][1], buttonStrings[curr][2], buttonStrings[curr][3], WHITE)

def processMouseEvents(event, prev, canLoad):
    # Time to start a new game
    if newGameBox.collidepoint(event.pos):
        redrawButton(prev, 0)
        return 0, True
    # Load an existing game or not do anything if no save file
    if continueGameBox.collidepoint(event.pos) and canLoad:
        redrawButton(prev, 1)
        return 1, True
    # Low difficulty selected
    if lowDiffBox.collidepoint(event.pos):
        chooseDifficulty(0.5)
        shared.difficulty = 0.5
        return 2, True
    # medium difficulty selected
    if medDiffBox.collidepoint(event.pos):
        chooseDifficulty(1)
        shared.difficulty = 1
        return 2, True
    # high difficuly selected
    if hiDiffBox.collidepoint(event.pos):
        chooseDifficulty(1.5)
        shared.difficulty = 1.5
        return 2, True
    # open the high scores screen
    if highScoresBox.collidepoint(event.pos):
        redrawButton(prev, 3)
        return 3, True
    # quit the game from the quit button in the menu
    if quitBox.collidepoint(event.pos):
        redrawButton(prev, 4)
        return 4, True

def processKeyEvents(event, prev, canLoad):
    if event.key == pygame.K_RETURN:
        return prev, True
    curr = prev
    if curr == 2:
        if event.key == pygame.K_LEFT or event.key == ord('a'):
            if shared.difficulty>0.5:
                colourBox(curr, GRAY, shared.difficulty)
                shared.difficulty -= 0.5
                colourBox(curr, WHITE, shared.difficulty)
                chooseDifficulty(shared.difficulty)
        elif event.key == pygame.K_RIGHT or event.key == ord('d'):
            if shared.difficulty<1.5:
                colourBox(curr, GRAY, shared.difficulty)
                shared.difficulty += 0.5
                colourBox(curr, WHITE, shared.difficulty)
                chooseDifficulty(shared.difficulty)
    if event.key == pygame.K_UP or event.key == ord('w'):
        if prev == 0:
            curr == 4
        else:
            curr -= 1
        if not canLoad and curr == 1:
            curr = 0
    elif event.key == pygame.K_DOWN or event.key == ord('s'):
        if prev == 4:
            curr == 0
        else:
            curr += 1
        if not canLoad and curr == 1:
            curr = 2

    if prev != curr:
        if prev == 2:
            colourBox(2, GRAY, shared.difficulty)
        else:
            colourBox(prev, GRAY)

        if curr == 2:
            colourBox(2, WHITE, shared.difficulty)
        else:
            colourBox(curr, WHITE)

    else:
        colourBox(curr, WHITE)
        colourBox(prev, GRAY)

    redrawButton(prev, curr)

    return curr, False

def sequence():
    exit = False
    quit = False
    initMenuScreen = True
    toStart = False
    toHighScore = False
    canLoad = False
    prev = 0
    while not exit:
        if initMenuScreen:
            canLoad = drawMenuScreen()
            initMenuScreen = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
                quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                prev, exit = processMouseEvents(event, prev, canLoad)
            elif event.type == pygame.KEYDOWN:
                prev, exit = processKeyEvents(event, prev, canLoad)


    if prev == 4 or quit:
        pygame.quit()
        sys.exit()

    if prev == 0:
        return 1
    if prev == 3:
        return 0
    if prev == 1:
        return 2
