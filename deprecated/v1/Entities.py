import pygame
from abc import ABC, abstractmethod

YELLOW = (255, 255, 0)


class Universe:
    """
    Class representing the silty universe
    """

    def __init__(self, display):
        self.display = display
        self.entities = []

    def update(self):
        pixels = pygame.PixelArray(self.display)
        for entity in self.entities:
            entity.update()
            pixels[entity.x][entity.y] = entity.color

        pixels.close()

    def brush(self):
        """
        Tool for drawing silt into the universe
        """
        size = 1
        x, y = pygame.mouse.get_pos()
        for x in range(x - size, x + size):
            for y in range(y - size, y + size):
                if x < self.display.get_width() and y < self.display.get_height():
                    self.entities.append(Silt(x, y, YELLOW, self))


class Ent(ABC):
    """
    Base class for all entities in the silt universe
    """

    def __init__(self, x, y, color, universe):
        self.x = x  # x pos
        self.y = y  # y pos
        self.color = color  # color
        self.universe = universe  # universe

    def get_neighbors(self) -> dict:
        """
        Return a list of neighbors
        """
        neighbors = {}
        for entity in self.universe.entities:
            if entity is not self:
                # North Neighbor
                if entity.x == self.x and entity.y == self.y - 1:
                    neighbors["N"] = entity
                # South Neighbor
                if entity.x == self.x and entity.y == self.y + 1:
                    neighbors["S"] = entity
                # East Neighbor
                if entity.x == self.x + 1 and entity.y == self.y:

                    neighbors["E"] = entity
                # West Neighbor
                if entity.x == self.x - 1 and entity.y == self.y:
                    neighbors["W"] = entity
                # North East Neighbor
                if entity.x == self.x + 1 and entity.y == self.y - 1:
                    neighbors["NE"] = entity
                # North West Neighbor
                if entity.x == self.x - 1 and entity.y == self.y - 1:
                    neighbors["NW"] = entity

                # South East Neighbor
                if entity.x == self.x + 1 and entity.y == self.y + 1:
                    neighbors["SE"] = entity
                # South West Neighbor
                if entity.x == self.x - 1 and entity.y == self.y + 1:
                    neighbors["SW"] = entity
                return neighbors
        return neighbors

    @abstractmethod
    def update(self):
        """
        Update the entity
        """
        pass


class GraviticSolid(Ent):
    """
    A solid entity that is affected by gravity
    """

    def update(self):
        """
        Update the entity
        """
        if self.y < self.universe.display.get_height() - 1:
            self.y += 1


class Silt(GraviticSolid):
    """
    A silty entity
    """

    def update(self):
        """
        Update the entity
        """
        done = False
        breakpoint()
        while not done:
            neighbors = self.get_neighbors()
            # fall if there are no southern neighbors and we're not at the edge of the map
            if (
                not neighbors.get("S")
                and self.y < self.universe.display.get_height() - 1
            ):
                self.y += 1

            # if there are eastern but no western neighbors
            elif neighbors.get("E") and not neighbors.get("W"):
                self.x -= 1

            # vice versa
            elif neighbors.get("W") and not neighbors.get("E"):
                self.x += 1

            # if both east and west are free, randomly pick one
            elif neighbors.get("E") and neighbors.get("W"):
                if randrange(0, 1) >= 5:
                    self.x -= 1
                else:
                    self.x += 1
            else:
                done = True
