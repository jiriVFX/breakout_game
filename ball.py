import pygame
from constants import *
import time


class Ball(pygame.sprite.Sprite):
    # Paddle collision threshold determines whether the centre or corners of paddle were hit
    MID_THRESHOLD = 50
    CORNER_THRESHOLD = 20
    # Initialize the sound module
    pygame.mixer.init()
    collision_sound = pygame.mixer.Sound("static/sound/bat_hit.mp3")

    def __init__(self, ball_path, ball_radius=20, ball_color=white):
        super().__init__()
        try:
            self.surface = pygame.image.load(ball_path).convert_alpha()
            self.surface.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        except FileNotFoundError:
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

    def bounce_sound(self):
        self.collision_sound.play()

    def bounce(self):
        self.direction_y *= -1
        if self.bounce_count < 10:
            self.bounce_count += 1
        else:
            self.speed += 0.5
            self.bounce_count = 0
        # Play sound
        self.bounce_sound()

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
            # Play sound
            self.bounce_sound()
        elif self.corner.left < 5 or self.corner.right > GAME_WIDTH:
            self.direction_x *= - 1
            self.bounce_count += 1
            # Play sound
            self.bounce_sound()
        # If the ball gets beyond game field on the bottom
        elif self.corner.bottom > GAME_HEIGHT:
            print("You loose life")
            time.sleep(0.5)
            self.reset()
            # Play sound
            self.bounce_sound()

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
            #print(f"Paddle midtop: {paddle.corner.midtop[0]}")
            #print(f"Ball bottom: {self.corner.midbottom[0]}")
            # When the ball hits paddle in the middle
            if abs(self.corner.midbottom[0] - paddle.corner.midtop[0]) < self.MID_THRESHOLD and self.direction_y > 0:
                print("Hit centre")
                self.direction_y *= - 1
                # If the paddle is moving the same direction as the ball
                if (self.direction_x > 0 and paddle.direction > 0) or (self.direction_x < 0 and paddle.direction < 0):
                    if self.speed < 5:
                        self.speed += 0.5
                        print(f"Paddle direction: {paddle.direction}")
                        print(f"Ball direction_x: {self.direction_x}")
                # If paddle and ball are moving opposite directions
                elif (self.direction_x > 0 > paddle.direction) or (self.direction_x < 0 < paddle.direction):
                    if self.speed > 2:
                        self.speed -= 0.5
                        print(f"Paddle direction: {paddle.direction}")
                        print(f"Ball direction_x: {self.direction_x}")
            else:
                # When left edge of the paddle was hit
                self.direction_y *= - 1

                if abs(self.corner.midbottom[0] - paddle.corner.topleft[0]) < self.CORNER_THRESHOLD:
                    # If the paddle moves in the opposite direction to ball
                    if self.direction_x > 0 and paddle.direction == -1:
                        self.direction_x *= -1
                    print("Hit left corner")
                # When the right edge of the paddle was hit
                elif abs(self.corner.midbottom[0] - paddle.corner.topright[0]) < self.CORNER_THRESHOLD:
                    # If the paddle moves in the opposite direction to ball
                    if self.direction_x < 0 and paddle.direction == 1:
                        self.direction_x *= -1
                    print("Hit right corner")
            print(f"Ball speed: {self.speed}")
            # Play sound
            self.bounce_sound()
