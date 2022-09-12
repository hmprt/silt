"""
A simple silt sim which draws only sand
"""
import time
import pygame

pygame.init()


class Universe:
    """A silty universe"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.surface = pygame.surface.Surface((x, y))
        self.state = [[None for y in range(y)] for x in range(x)]
        self.next_state = [[None for y in range(y)] for x in range(x)]

    def step(self):
        """
        Update all particles, ready for redraw
        """
        for x in range(self.x):
            for y in range(self.y):
                if self.state[x][y] is None:
                    continue
                if not self.state[x][y].updated:
                    self.state[x][y].update()

        self.state = self.next_state
        self.next_state = [[None for y in range(self.y)] for x in range(self.x)]


class Silt:
    """A silt particle"""

    def __init__(self, x, y, universe, falling=False):
        self.x = x
        self.y = y
        self.universe = universe
        self.color = (255, 255, 0)
        self.type = "silt"
        self.updated = (
            False  # whether this particle was updated in the most recent step
        )
        self.falling = falling

    def update(self):
        """Updated the state of this particle"""
        state = universe.state
        next_state = universe.next_state

        ## Vertical movement
        # see if the particle is falling
        if self.y == universe.y - 1:
            next_state[self.x][self.y] = self
            self.falling = False
            return

        # fall if the below particle is falling
        if state[self.x][self.y + 1] is not None:
            state[self.x][self.y + 1].update()
            if state[self.x][self.y + 1].falling:
                self.falling = True
                next_state[self.x][self.y + 1] = Silt(self.x, self.y + 1, universe)
                return

        if state[self.x][self.y + 1] is None:
            next_state[self.x][self.y + 1] = Silt(self.x, self.y + 1, universe)
            self.falling = True
            return

        ## Horizontal Movement (southwest)
        if not self.x == 0 and not self.y == universe.y - 1:
            if state[self.x][self.y + 1] and state[self.x - 1][self.y + 1] is None:
                next_state[self.x - 1][self.y + 1] = Silt(
                    self.x - 1, self.y + 1, universe
                )
                self.falling = True
                return
        ## Horizontal Movement (southeast)
        if not self.x == universe.x - 1 and not self.y == universe.y - 1:
            if state[self.x][self.y + 1] and state[self.x + 1][self.y + 1] is None:
                next_state[self.x + 1][self.y + 1] = Silt(
                    self.x + 1, self.y + 1, universe
                )
                self.falling = True
                return
        

        # finally, assume we just stay in place
        next_state[self.x][self.y] = self


# main event loop
if __name__ == "__main__":

    # display init
    display_surface = pygame.display.set_mode((500, 500))

    # universe init
    universe = Universe(130, 130)
    for x in range(75, 110):
        for y in range(17, 40):
            universe.state[x][y] = Silt(x, y, universe)
    # core loop init
    done = False
    while not done:
        pixels = pygame.PixelArray(universe.surface)
        for x in range(universe.x):
            for y in range(universe.y):
                if universe.state[x][y]:
                    pixels[x][y] = universe.state[x][y].color
                else:
                    pixels[x][y] = (0, 0, 0)
        pygame.transform.scale(universe.surface, (500, 500), display_surface)
        pygame.display.flip()
        universe.step()
