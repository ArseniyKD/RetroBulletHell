import pygame
import sys
import os
import shared
import time
import HighScoreTracking

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((shared.width, shared.height))
screen.fill(shared.BLACK)
backdropbox = screen.get_rect()
hs = HighScoreTracking.HighScore()

input_box = pygame.Rect(shared.width / 2, 400, 250, 40)
continue_box = pygame.Rect(75, 495, 345, 85)

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
    text_to_screen(screen, "GAME OVER", shared.width / 5 - 25, shared.height / 5, 75, shared.GOLD)
    text_to_screen(screen, 'YOUR SCORE IS  {0}'.format(shared.score), shared.width / 10 - 30, shared.height / 3, 50, shared.GOLD)
    text_to_screen(screen, 'Enter  Name  ', 25, 400, 40, shared.GOLD)
    text_to_screen(screen, 'CONTINUE', 85,  500, 75, shared.GOLD)
    pygame.draw.rect(screen, shared.WHITE, continue_box, 3)


def gameOverInput(event):
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
        # elif event.key == pygame.K_RETURN:
        #     return True
        elif len(shared.playerName) < 11:
            if event.unicode == ' ':
                shared.playerName += '_'
            else:
                shared.playerName += event.unicode

    pygame.draw.rect(screen, shared.BLACK, input_box)
    text_to_screen(screen, shared.playerName, input_box.x, input_box.y, 40, shared.GOLD)
    return False

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
