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
hs = HighScoreTracking.HighScore()

input_box = pygame.Rect(shared.width / 2, 400, 250, 40)
continue_box = pygame.Rect(75, 495, 345, 85)

def gameOverSequence():
    text_to_screen(screen, 'GAME OVER', shared.width / 5 - 25, shared.height / 5, 75, shared.GOLD)
    time.sleep(0.50)
    text_to_screen(screen, 'GAME OVER', shared.width / 5 - 25, shared.height / 5, 75, shared.WHITE)
    time.sleep(0.25)
    text_to_screen(screen, 'GAME OVER', shared.width / 5 - 25, shared.height / 5, 75, shared.GOLD)
    time.sleep(0.50)
    screen.fill(shared.BLACK)
    pygame.display.update()
    '''
    text_to_screen(screen, 'GAME OVER', shared.width / 5 - 25, shared.height / 5, 75, WHITE)
    time.sleep(0.25)
    text_to_screen(screen, "GAME OVER", shared.width / 5 - 25, shared.height / 5, 75, GOLD)
    time.sleep(1)
    screen.fill(BLACK)
    pygame.display.update()
    time.sleep(0.25)
    '''
    score = str(shared.score)
    scoreVal = ''

    for c in score:
        if c == '-':
            scoreVal += 'N'
        else:
            scoreVal += c

    text_to_screen(screen, "GAME OVER", shared.width / 5 - 25, shared.height / 5, 75, shared.GOLD)
    text_to_screen(screen, 'YOUR SCORE IS  {0}'.format(scoreVal), shared.width / 10 - 30, shared.height / 3, 50, shared.GOLD)
    text_to_screen(screen, 'Enter  Name  ', 25, 400, 40, shared.GOLD)
    text_to_screen(screen, 'CONTINUE', 85,  500, 75, shared.GOLD)
    pygame.draw.rect(screen, shared.WHITE, continue_box, 3)


def sequence():
    quit = False
    exit = False
    initGameOverScreen = True
    while not exit:
        if initGameOverScreen:
            gameOverSequence()
            initGameOverScreen = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
                quit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_box.collidepoint(event.pos):
                    hs.ScoreKeeping(shared.score)
                    shared.score = 0
                    if shared.playerName == '':
                        hs.updateHighScoresFile('DEFAULT')
                    else:
                        hs.updateHighScoresFile(shared.playerName)
                    return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    shared.playerName = shared.playerName[:-1]
                elif event.key == pygame.K_RETURN:
                    hs.ScoreKeeping(shared.score)
                    shared.score = 0
                    if shared.playerName == '':
                        hs.updateHighScoresFile('DEFAULT')
                    else:
                        hs.updateHighScoresFile(shared.playerName)
                    return True
                elif len(shared.playerName) < 11:
                    if event.unicode == ' ':
                        shared.playerName += '_'
                    else:
                        shared.playerName += event.unicode

            playerName = ''
            for c in shared.playerName:
                if c == '_':
                    playerName += '   '
                else:
                    playerName += c
            pygame.draw.rect(screen, shared.BLACK, input_box)
            text_to_screen(screen, playerName, input_box.x, input_box.y, 40, shared.GOLD)
    if quit:
        pygame.quit()
        sys.exit()
    # if event.type == pygame.MOUSEBUTTONDOWN:
    #     if continue_box.collidepoint(event.pos):
    #         hs.ScoreKeeping(shared.score)
    #         shared.score = 0
    #         if shared.playerName == '':
    #             hs.updateHighScoresFile('DEFAULT')
    #         else:
    #             hs.updateHighScoresFile(shared.playerName)
    #         return True
    # if event.type == pygame.KEYDOWN:
    #     if event.key == pygame.K_BACKSPACE:
    #         shared.playerName = shared.playerName[:-1]
    #     # elif event.key == pygame.K_RETURN:
    #     #     return True
    #     elif len(shared.playerName) < 11:
    #         if event.unicode == ' ':
    #             shared.playerName += '_'
    #         else:
    #             shared.playerName += event.unicode
    #
    # pygame.draw.rect(screen, shared.BLACK, input_box)
    # text_to_screen(screen, shared.playerName, input_box.x, input_box.y, 40, shared.GOLD)
    # return False
'''
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if continue_box.collidepoint(event.pos):
                print(name)
                print("This file is off to better things :D")
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
'''
