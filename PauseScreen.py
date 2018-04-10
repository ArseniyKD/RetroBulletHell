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

pauseScreenBox = pygame.Rect(shared.width/7, shared.width/7, shared.width/7*5, shared.height/3)
continueGameBox = pygame.Rect(shared.width/7+85, shared.width/7+70, 190, 40)
saveGameBox = pygame.Rect(shared.width/7+130, shared.width/7+122, 100, 40)
menuBox = pygame.Rect(shared.width/7+130, shared.width/7+175, 100, 40)

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


def processEvents(event):
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

# used the following resource to draw semi transparent box:
# https://stackoverflow.com/questions/17581545/drawn-surface-transparency-in-pygame
def drawPauseScreen():
    #s = pygame.Surface((shared.width/7*5, shared.height/3))
    ck = (127, 33, 33)
    s = pygame.Surface((shared.width, shared.height))
    s.fill(ck)
    s.set_colorkey(ck)
    pygame.draw.rect(s, shared.DARKBLUE, pauseScreenBox, 0)
    s.set_alpha(100)
    screen.blit(s, (0,0))

    text_to_screen(screen, "PAUSE MENU", shared.width/7+50, shared.width/7, 50, shared.GOLD)
    pygame.draw.line(screen, shared.WHITE, (shared.width/7, shared.width/7+50), (shared.width/7*6, shared.width/7+50), 2)
    text_to_screen(screen, "CONTINUE", shared.width/7+90, shared.width/7+70, 40, shared.GOLD)
    pygame.draw.rect(screen, shared.GRAY, continueGameBox , 3)
    text_to_screen(screen, "SAVE", shared.width/7+135, shared.width/7+122, 40, shared.GOLD)
    pygame.draw.rect(screen, shared.GRAY, saveGameBox , 3)
    text_to_screen(screen, "MENU", shared.width/7+135, shared.width/7+175, 40, shared.GOLD)
    pygame.draw.rect(screen, shared.GRAY, menuBox , 3)

    pygame.display.update()


def pauseSequence():
    exit = False
    quit = False
    initPauseScreen = True
    while not exit:
        if initPauseScreen:
            drawPauseScreen()
            initPauseScreen = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
                quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                processed = processEvents(event)
                exit = True

    if exit and quit:
        pygame.quit()
        sys.exit()

    return processed
