import pygame
from constants import *
import time


class Ball(pygame.sprite.Sprite):
    def __init__(self, ball_radius, ball_color):
        super().__init__()
        self.ball_radius = ball_radius
        self.surface = pygame.Surface((self.ball_radius, self.ball_radius))
        self.surface.fill(ball_color)
        # Top left corner position coordinates
        self.corner = self.surface.get_rect(center=(GAME_WIDTH / 2, GAME_HEIGHT - 55))
        # Make correct collision circle around the ball
        self.radius = self.corner.width / 2
        self.direction_x = -1
        self.direction_y = -1
        self.speed = 2
        self.bounce_count = 0

    def move(self):
        self.corner.move_ip(self.direction_x * self.speed, self.direction_y * self.speed)

    def bounce(self):
        self.direction_y *= -1
        if self.bounce_count < 10:
            self.bounce_count += 1
        else:
            self.speed += 0.5
            self.bounce_count = 0

    def reset(self):
        self.corner = self.surface.get_rect(center=(GAME_WIDTH / 2, GAME_HEIGHT - 55))
        self.direction_x = -1
        self.direction_y = -1
        self.speed = 2

    def border_collision(self):
        # Bounce ball of the walls
        if self.corner.top < 5:
            self.direction_y *= - 1
            self.bounce_count += 1
        elif self.corner.left < 5 or self.corner.right > GAME_WIDTH:
            self.direction_x *= - 1
            self.bounce_count += 1
        # If the ball gets beyond game field on the bottom
        elif self.corner.bottom > GAME_HEIGHT:
            print("You loose life")
            time.sleep(0.5)
            self.reset()

    def collision_detect(self, wall_group, paddle):
        # Handle border sides collisions
        self.border_collision()

        # Wall collision detection
        for brick in wall_group:
            if self.corner.colliderect(brick.corner):
                brick.kill()
                self.bounce()

        # Paddle collision detection
        if self.corner.colliderect(paddle.corner):
            # When the ball hits paddle in the middle
            if abs(self.corner.bottom - paddle.corner.top) < 1 and self.direction_y > 0:
                self.direction_y *= - 1
                # If the paddle is moving the same direction as the ball
                if (self.direction_x > 0 and paddle.direction > 0) or (self.direction_x < 0 and paddle.direction < 0):
                    if self.speed < 5:
                        self.speed += 0.5
                        print(paddle.direction)
                        print(self.direction_x)
                # If paddle and ball are moving opposite directions
                elif (self.direction_x > 0 > paddle.direction) or (self.direction_x < 0 < paddle.direction):
                    if self.speed > 2:
                        self.speed -= 0.5
                        print(paddle.direction)
                        print(self.direction_x)
            else:
                if self.direction_y > 0:
                    self.direction_y *= - 1
                    # ball.direction_x *= - 1
                    print("Hit corners")
                    print(self.direction_x)
            print(self.speed)
