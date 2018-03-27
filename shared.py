import pygame

width = 500
height = 700
imgWidth = 39
imgHeight = 43
step = 10  # step is the number of pixels the character moves each key press
bulletStep = 12
fps = 60
clock = pygame.time.Clock()
bullets = [] # list of bullets
