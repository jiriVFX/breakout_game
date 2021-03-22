import pygame
from constants import *


class Brick(pygame.sprite.Sprite):
    def __init__(self, position_x, position_y, brick_color):
        super().__init__()
        self.width = GAME_WIDTH / 10 - 5
        self.height = GAME_HEIGHT / 30
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(brick_color)
        # Top left corner position coordinates
        self.corner = self.surface.get_rect(center=(position_x, position_y))
