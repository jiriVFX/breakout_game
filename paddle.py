import pygame
from constants import *


class Paddle(pygame.sprite.Sprite):
    def __init__(self, paddle_width, paddle_height, paddle_color):
        super().__init__()
        self.width = paddle_width
        self.height = paddle_height
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(paddle_color)
        # Top left corner position coordinates
        self.corner = self.surface.get_rect(center=((GAME_WIDTH) / 2, GAME_HEIGHT - 40))
        self.speed = 5
        self.direction = 0

    def move(self, pressed_keys):
        self.direction = 0
        if pressed_keys[pygame.K_LEFT]:
            self.corner.move_ip(-self.speed, 0)
            self.direction = - 1
        if pressed_keys[pygame.K_RIGHT]:
            self.corner.move_ip(self.speed, 0)
            self.direction = 1
        #print(self.corner)

        if self.corner.left < 5:
            self.corner.left = 5
        if self.corner.right > SCREEN_WIDTH - 5:
            self.corner.right = SCREEN_WIDTH - 5