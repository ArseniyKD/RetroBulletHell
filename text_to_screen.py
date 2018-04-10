import pygame
import sys

# got this function from https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame
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
