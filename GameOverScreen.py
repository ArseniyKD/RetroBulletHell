# Created by Arseniy Kouzmenkov 1542302 and Patrisha de Boon 1496979

import pygame
import sys
import os
import shared
import time
import HighScoreTracking
from text_to_screen import text_to_screen

# the initialisation calls for pygame and the current screen along with the highs score tracking class.
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((shared.width, shared.height))
screen.fill(shared.BLACK)
backdropbox = screen.get_rect()
hs = HighScoreTracking.HighScore()

# the initialisation for the input box and the continue button.
input_box = pygame.Rect(shared.width / 2, 400, 250, 40)
continue_box = pygame.Rect(75, 495, 345, 85)

# the sequence that draws the initial game over screen.
def gameOverSequence():
    # this flashes game over on the screen without filling the screen with black
    # so that the user can see the exact moment and location of the final hit.
    text_to_screen(screen, 'GAME OVER', shared.width / 5 - 25, shared.height / 5, 75, shared.GOLD)
    time.sleep(0.50)
    text_to_screen(screen, 'GAME OVER', shared.width / 5 - 25, shared.height / 5, 75, shared.WHITE)
    time.sleep(0.25)
    text_to_screen(screen, 'GAME OVER', shared.width / 5 - 25, shared.height / 5, 75, shared.GOLD)
    time.sleep(0.50)
    screen.fill(shared.BLACK)
    pygame.display.update()

    # the reason for converting the score to a string is because you can get a negative value for your score
    # in the game. The font we are using does not have a dash, so we have to represent negative scores
    # with a capital letter 'N' in the final output of the score.
    score = str(shared.score)
    scoreVal = ''
    for c in score:
        if c == '-':
            scoreVal += 'N'
        else:
            scoreVal += c

    # this part draws the rest of the game over screen.
    text_to_screen(screen, "GAME OVER", shared.width / 5 - 25, shared.height / 5, 75, shared.GOLD)
    text_to_screen(screen, 'YOUR SCORE IS  {0}'.format(scoreVal), shared.width / 10 - 30, shared.height / 3, 50, shared.GOLD)
    text_to_screen(screen, 'Enter  Name  ', 25, 400, 40, shared.GOLD)
    text_to_screen(screen, 'CONTINUE', 85,  500, 75, shared.GOLD)
    pygame.draw.rect(screen, shared.WHITE, continue_box, 3)

# this function is the entire game over sequence.
def sequence():
    # initialise certain variables to run the sequence.
    # exit will continue to the next screen (the high score screen)
    # while quit will close the game.
    quit = False
    exit = False
    initGameOverScreen = True
    while not exit:
        # this needs to run only once in order to draw the screen itself.
        if initGameOverScreen:
            gameOverSequence()
            initGameOverScreen = False

        # this will go through all the events within the game.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
                quit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if the player clicks on the continue button, the high score gets saved
                # and depending on the value of the player name, will either set the
                # name to "Default" or to the chosen player name.
                if continue_box.collidepoint(event.pos):
                    hs.ScoreKeeping(shared.score)
                    shared.score = 0
                    if shared.playerName == '':
                        hs.updateHighScoresFile('DEFAULT')
                    else:
                        hs.updateHighScoresFile(shared.playerName)
                    return True

            if event.type == pygame.KEYDOWN:
                # this will get rid of the last character of the player name if
                # backspace is pressed.
                if event.key == pygame.K_BACKSPACE:
                    shared.playerName = shared.playerName[:-1]

                # if the enter button is hit, the high score gets saved
                # and depending on the value of the player name, will either set the
                # name to "Default" or to the chosen player name.
                elif event.key == pygame.K_RETURN:
                    hs.ScoreKeeping(shared.score)
                    shared.score = 0
                    if shared.playerName == '':
                        hs.updateHighScoresFile('DEFAULT')
                    else:
                        hs.updateHighScoresFile(shared.playerName)
                    return True

                # because of the way that the highScore file stores the names, we cannot
                # use spaces in the name. Thus, the spaces get changed to underscores so that
                # they can get stored properly.
                # if the length of the input exceeds 10 characters, no more input will be processed until
                # backspace gets hit.
                elif len(shared.playerName) < 11:
                    if event.unicode == ' ':
                        shared.playerName += '_'
                    else:
                        shared.playerName += event.unicode

            # the underscore character does not exist in out font, we change the underscores to
            # spaces when drawing the characters to the screen.
            playerName = ''
            for c in shared.playerName:
                if c == '_':
                    playerName += '   '
                else:
                    playerName += c
            pygame.draw.rect(screen, shared.BLACK, input_box)
            text_to_screen(screen, playerName, input_box.x, input_box.y, 40, shared.GOLD)

    # this closes the window if the "close window" button gets hit.
    if quit:
        pygame.quit()
        sys.exit()
