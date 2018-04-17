# Created by Arseniy Kouzmenkov 1542302 and Patrisha de Boon 1496979

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

# this block creates all the boxes for the buttons in the pause screen.
pauseScreenBox = pygame.Rect(shared.width/7, shared.width/7, shared.width/7*5, shared.height/3)
continueGameBox = pygame.Rect(shared.width/7+85, shared.width/7+70, 190, 40)
saveGameBox = pygame.Rect(shared.width/7+130, shared.width/7+122, 100, 40)
menuBox = pygame.Rect(shared.width/7+130, shared.width/7+175, 100, 40)

# this colours the outline of the currently selected option in the pause screen.
def colourBox(curr, colour):
    if curr == 1:
        pygame.draw.rect(screen, colour, continueGameBox, 3)
    elif curr == 2:
        pygame.draw.rect(screen, colour, saveGameBox, 3)
    elif curr == 3:
        pygame.draw.rect(screen, colour, menuBox, 3)

# this function redraws the buttons when using the arrowkeys to navigate the pause screen.
def redrawButton(prev, curr):
    if prev != curr:
        buttonStrings = {1:("CONTINUE", shared.width/7+90, shared.width/7+70, 40), 2:("SAVE", shared.width/7+135, shared.width/7+122, 40), 3:("MENU", shared.width/7+135, shared.width/7+175, 40)}
        text_to_screen(screen, buttonStrings[prev][0], buttonStrings[prev][1], buttonStrings[prev][2], buttonStrings[prev][3], shared.GOLD)
        text_to_screen(screen, buttonStrings[curr][0], buttonStrings[curr][1], buttonStrings[curr][2], buttonStrings[curr][3], shared.WHITE)

# this function processes pause screen navigation using the mouse clicks.
def processMouseEvents(event):
    if  continueGameBox.collidepoint(event.pos):
        text_to_screen(screen, "CONTINUE", shared.width/7+90, shared.width/7+70, 40, shared.WHITE)
        pygame.draw.rect(screen, shared.WHITE, continueGameBox , 3)
        pygame.display.update()
        return 1
    if  saveGameBox.collidepoint(event.pos):
        text_to_screen(screen, "SAVE", shared.width/7+135, shared.width/7+122, 40, shared.WHITE)
        pygame.draw.rect(screen, shared.WHITE, saveGameBox , 3)
        pygame.display.update()
        return 2
    if  menuBox.collidepoint(event.pos):
        text_to_screen(screen, "MENU", shared.width/7+135, shared.width/7+175, 40, shared.WHITE)
        pygame.draw.rect(screen, shared.WHITE, menuBox , 3)
        pygame.display.update()
        return 3

# this processes the arrowkey movement in the pause screen.
def processKeyEvents(event, prev):
    if event.key == pygame.K_RETURN:
        return prev, True
    curr = prev
    if event.key == pygame.K_UP or event.key == ord('w'):
        if prev == 1:
            curr = 3
        else:
            curr -= 1
    elif event.key == pygame.K_DOWN or event.key == ord('s'):
        if prev == 3:
            curr = 1
        else:
            curr += 1

    colourBox(curr, shared.WHITE)
    colourBox(prev, shared.GRAY)

    redrawButton(prev, curr)

    return curr, False

# used the following resource to draw semi transparent box:
# https://stackoverflow.com/questions/17581545/drawn-surface-transparency-in-pygame
def drawPauseScreen():
    # draws a partially transparent light blue background only for the pause screen section of the screen
    ck = (127, 33, 33)
    s = pygame.Surface((shared.width, shared.height))
    s.fill(ck)
    s.set_colorkey(ck)
    pygame.draw.rect(s, shared.DARKBLUE, pauseScreenBox, 0)
    s.set_alpha(200)
    screen.blit(s, (0,0))

    # draws the buttons within that portion of the screen.
    text_to_screen(screen, "PAUSE MENU", shared.width/7+50, shared.width/7, 50, shared.GOLD)
    pygame.draw.line(screen, shared.WHITE, (shared.width/7, shared.width/7+50), (shared.width/7*6, shared.width/7+50), 2)
    text_to_screen(screen, "CONTINUE", shared.width/7+90, shared.width/7+70, 40, shared.WHITE)
    pygame.draw.rect(screen, shared.WHITE, continueGameBox , 3)
    text_to_screen(screen, "SAVE", shared.width/7+135, shared.width/7+122, 40, shared.GOLD)
    pygame.draw.rect(screen, shared.GRAY, saveGameBox , 3)
    text_to_screen(screen, "MENU", shared.width/7+135, shared.width/7+175, 40, shared.GOLD)
    pygame.draw.rect(screen, shared.GRAY, menuBox , 3)

    pygame.display.update()

# this function runs the pause screen sequence during the game.
def pauseSequence():
    # exit lets the game continue,
    # quit closes the window.
    exit = False
    quit = False
    initPauseScreen = True
    prev = 1
    processed = None
    while not exit:
        # needs to run only once to draw the pause screen.
        if initPauseScreen:
            drawPauseScreen()
            initPauseScreen = False

        # processes all the events within this sequence.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
                quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                processed = processMouseEvents(event)
                exit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    processed = 1
                    exit = True
                else:
                    prev, exit = processKeyEvents(event, prev)

    # closes the window.
    if exit and quit:
        pygame.quit()
        sys.exit()

    # if the escape button is hit, continues the game.
    if processed is not None:
        return processed
    else:
        return prev
