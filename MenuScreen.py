import pygame
import sys
import os
import shared
import time
from text_to_screen import text_to_screen

# the initialisation calls for pygame and the current screen.
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((shared.width, shared.height))
screen.fill(shared.BLACK)
backdropbox = screen.get_rect()

# this block creates all the boxes for the buttons in the menu.
newGameBox = pygame.Rect(100, 105, 315, 85)
continueGameBox = pygame.Rect(10, 205, 490, 80)
lowDiffBox = pygame.Rect(40, 385, 100, 60)
medDiffBox = pygame.Rect(155, 385, 180, 60)
hiDiffBox = pygame.Rect(340, 385, 130, 60)
highScoresBox = pygame.Rect(30, 460, 435, 85)
quitBox = pygame.Rect(150, 580, 175, 85)

# the background image came from here:
# https://pxhere.com/en/photo/610854
def drawMenuScreen():
    # this creates the background for the screen.
    BGimage = pygame.image.load(os.path.join('images','menuBG.png')).convert()
    screen.blit(BGimage, (0,0))

    # this part creates all the graphic for the menu screen, drawing
    # all the buttons and all the text on the screen.
    text_to_screen(screen, "RETRO", 30, 20, 50, shared.GOLD)
    text_to_screen(screen, "BULLET", 190, 20, 50, shared.BLUE)
    text_to_screen(screen, "HELL", 370, 20, 50, shared.RED)
    pygame.draw.line(screen, shared.WHITE, (0, 80), (shared.width, 80), 2)
    text_to_screen(screen, "NEW GAME", 110, 50 + 60, 75, shared.WHITE)
    pygame.draw.rect(screen, shared.WHITE, newGameBox, 3)

    # this block grays out the "Continue Game" button if there is no save file
    # present within the directory.
    # can load is then stored for the sake of keeping track whether the box is
    # used at all or not.
    canLoad = False
    try:
        istream = open('save.txt', 'r').close()
        canLoad = True
    except:
        text_to_screen(screen, "CONTINUE GAME", 15, 150 + 60, 70, shared.GRAY)
    if canLoad:
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

    return canLoad

# this function will colour the correct difficulty setting's box outline.
# the selected difficuly is outlined in white, the rest are outlined in gray
def colourBox(curr, colour, diffLevel = shared.difficulty):
    if curr == 0:
        pygame.draw.rect(screen, colour, newGameBox, 3)
    elif curr == 1:
        pygame.draw.rect(screen, colour, continueGameBox, 3)
    elif curr == 2:
        if diffLevel == 1:
            pygame.draw.rect(screen, colour, lowDiffBox, 3)
        elif diffLevel == 2:
            pygame.draw.rect(screen, colour, medDiffBox, 3)
        elif diffLevel == 3:
            pygame.draw.rect(screen, colour, hiDiffBox, 3)
    elif curr == 3:
        pygame.draw.rect(screen, colour, highScoresBox, 3)
    elif curr == 4:
        pygame.draw.rect(screen, colour, quitBox, 3)

# this function colours the selected difficulty setting's text to white
# while keeping all the other choices golden
def chooseDifficulty(diffLevel):
    if diffLevel == 1:
        text_to_screen(screen, "LOW", 50, 330 + 60, 50, shared.WHITE)
        text_to_screen(screen, "MEDIUM", 160, 330 + 60, 50, shared.GOLD)
        text_to_screen(screen, "HIGH", 350, 330 + 60, 50, shared.GOLD)
    if diffLevel == 2:
        text_to_screen(screen, "LOW", 50, 330 + 60, 50, shared.GOLD)
        text_to_screen(screen, "MEDIUM", 160, 330 + 60, 50, shared.WHITE)
        text_to_screen(screen, "HIGH", 350, 330 + 60, 50, shared.GOLD)
    if diffLevel == 3:
        text_to_screen(screen, "LOW", 50, 330 + 60, 50, shared.GOLD)
        text_to_screen(screen, "MEDIUM", 160, 330 + 60, 50, shared.GOLD)
        text_to_screen(screen, "HIGH", 350, 330 + 60, 50, shared.WHITE)

# this function redraws the buttons when using the arrowkeys to
# navigate the menu.
def redrawButton(prev, curr):
    if prev != curr:
        buttonStrings = {0:("NEW GAME", 110, 50 + 60, 75), 1:("CONTINUE GAME", 15, 150 + 60, 70), 2:("DIFFICULTY", 50, 250 + 60, 75), 3:("HIGH SCORES", 40, 410 + 60, 75), 4: ("QUIT", 160, 530 + 60, 75)}
        text_to_screen(screen, buttonStrings[prev][0], buttonStrings[prev][1], buttonStrings[prev][2], buttonStrings[prev][3], shared.GOLD)
        if curr != 2:
            text_to_screen(screen, buttonStrings[curr][0], buttonStrings[curr][1], buttonStrings[curr][2], buttonStrings[curr][3], shared.WHITE)

# this processes the arrowkey movement in the menu screen.
def processKeyEvents(event, prev, canLoad):
    curr = prev
    if curr == 2:
        if event.key == pygame.K_LEFT or event.key == ord('a'):
            if shared.difficulty>1:
                colourBox(curr, shared.GRAY, shared.difficulty)
                shared.difficulty -= 1
                colourBox(curr, shared.WHITE, shared.difficulty)
                chooseDifficulty(shared.difficulty)
        elif event.key == pygame.K_RIGHT or event.key == ord('d'):
            if shared.difficulty<3:
                colourBox(curr, shared.GRAY, shared.difficulty)
                shared.difficulty += 1
                colourBox(curr, shared.WHITE, shared.difficulty)
                chooseDifficulty(shared.difficulty)
    else:
        if event.key == pygame.K_RETURN:
            return prev, True
    if event.key == pygame.K_UP or event.key == ord('w'):
        if prev == 0:
            curr = 4
        else:
            curr -= 1
        if not canLoad and curr == 1:
            curr = 0
    elif event.key == pygame.K_DOWN or event.key == ord('s'):
        if prev == 4:
            curr = 0
        else:
            curr += 1
        if not canLoad and curr == 1:
            curr = 2

    if prev != curr:
        if prev == 2:
            colourBox(2, shared.GRAY, shared.difficulty)
        else:
            colourBox(prev, shared.GRAY)
        if curr == 2:
            colourBox(2, shared.WHITE, shared.difficulty)
        else:
            colourBox(curr, shared.WHITE)

    else:
        colourBox(curr, shared.WHITE)
        colourBox(prev, shared.GRAY)

    redrawButton(prev, curr)

    return curr, False

# this function processes menu navigation using the mouse clicks.
def processMouseEvents(event, canLoad):
    # Time to start a new game
    if  newGameBox.collidepoint(event.pos):
        text_to_screen(screen, "NEW GAME", 110, 50 + 60, 75, shared.WHITE)
        colourBox(0, shared.WHITE)
        return 0, True
    # Load an existing game or not do anything if no save file
    if continueGameBox.collidepoint(event.pos) and canLoad:
        text_to_screen(screen, "CONTINUE GAME", 15, 150 + 60, 70, shared.WHITE)
        colourBox(1, shared.WHITE)
        return 1, True
    # Low difficulty selected
    if lowDiffBox.collidepoint(event.pos):
        colourBox(2, shared.GRAY, shared.difficulty)
        chooseDifficulty(1)
        shared.difficulty = 1
        colourBox(2, shared.WHITE, shared.difficulty)
        shared.enemyFireDelay = 1500
        return 2, False
    # medium difficulty selected
    if medDiffBox.collidepoint(event.pos):
        colourBox(2, shared.GRAY, shared.difficulty)
        chooseDifficulty(2)
        shared.difficulty = 2
        colourBox(2, shared.WHITE, shared.difficulty)
        shared.enemyFireDelay = 1000
        return 2, False
    # high difficuly selected
    if hiDiffBox.collidepoint(event.pos):
        colourBox(2, shared.GRAY, shared.difficulty)
        chooseDifficulty(3)
        shared.difficulty = 3
        colourBox(2, shared.WHITE, shared.difficulty)
        shared.enemyFireDelay = 750
        return 2, False
    # open the high scores screen
    if highScoresBox.collidepoint(event.pos):
        text_to_screen(screen, "HIGH SCORES", 40, 410 + 60, 75, shared.WHITE)
        colourBox(3, shared.WHITE)
        return 3, True
    # quit the game from the quit button in the menu
    if quitBox.collidepoint(event.pos):
        text_to_screen(screen, "QUIT", 160, 530 + 60, 75, shared.WHITE)
        colourBox(4, shared.WHITE)
        return 4, True

# this is the main menu sequence function. It will correctly pass the
# navigation requirements back to the FSM in RetroBulletHell.py .
# will also quit the game if the "Quit" button is clicked or the user clicks the
# close window button.
def sequence():
    exit = False
    quit = False
    initMenuScreen = True
    toStart = False
    toHighScore = False
    canLoad = False
    prev = 0
    while not exit:
        # this will run once just to draw the menu screen initially.
        if initMenuScreen:
            canLoad = drawMenuScreen()
            initMenuScreen = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
                quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                prev, exit = processMouseEvents(event, canLoad)
            elif event.type == pygame.KEYDOWN:
                prev, exit = processKeyEvents(event, prev, canLoad)

    if prev == 4 or quit:
        pygame.quit()
        sys.exit()

    # the returns make sense in the context of the FSM, please refer back to it for clarification.
    if prev == 0:
        return 1
    if prev == 1:
        return 2
    if prev == 3:
        return 0
