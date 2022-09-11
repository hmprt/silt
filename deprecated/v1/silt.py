import pygame
from Entities import Universe


# params
x = 500
y = 500

# pygame boilerplate
pygame.init()
display = pygame.display.set_mode((x, y))

# initialise the Universe
universe = Universe(display)

# initialise time
running = True

while running:

    # quit handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            universe.brush()
    universe.update()
    if universe.entities:
        universe.update()

    # core loop

    # update region (whole region for now)
    pygame.display.update()
