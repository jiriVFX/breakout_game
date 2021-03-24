import pygame
from constants import *
import time


class Ball(pygame.sprite.Sprite):
    # Paddle collision threshold determines whether the centre or corners of paddle were hit
    MID_THRESHOLD = 50
    CORNER_THRESHOLD = 20
    # Initialize the sound module
    pygame.mixer.init()
    col_sound = pygame.mixer.Sound("static/sound/hit1.mp3")
    col_sound_2 = pygame.mixer.Sound("static/sound/hit2.mp3")

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
        self.corner = self.surface.get_rect(center=(GAME_WIDTH / 2, GAME_HEIGHT - 60))
        # Make correct collision circle around the ball
        self.radius = self.corner.width / 2
        self.direction_x = -1
        self.direction_y = -1
        self.speed = MIN_SPEED
        self.bounce_count = 0

    def move(self):
        self.corner.move_ip(self.direction_x * self.speed, self.direction_y * self.speed)

    def bounce_sound(self):
        self.col_sound.play()

    def bounce_sound_2(self):
        self.col_sound_2.play()

    def speed_increase(self):
        if self.bounce_count < 10:
            self.bounce_count += 1
        elif self.speed < MAX_SPEED:
            self.speed += SPEED_INCREMENT
            self.bounce_count = 0
        else:
            self.bounce_count = 0

    def wall_bounce(self):
        self.direction_y *= -1
        self.speed_increase()
        # Play sound
        self.bounce_sound()

    def reset(self):
        self.corner = self.surface.get_rect(center=(GAME_WIDTH / 2, GAME_HEIGHT - 60))
        self.direction_x = -1
        self.direction_y = -1
        self.speed = MIN_SPEED
        self.bounce_count = 0

    def border_collision(self, scoreboard):
        # Bounce ball of the walls
        if self.corner.top < 5:
            self.direction_y *= - 1
            self.speed_increase()
            # Play sound
            self.bounce_sound()
        elif self.corner.left < 5 or self.corner.right > SCREEN_WIDTH - 5:
            self.direction_x *= - 1
            self.speed_increase()
            # Play sound
            self.bounce_sound()
        # If the ball gets beyond game field on the bottom
        elif self.corner.bottom > GAME_HEIGHT:
            print("Ball lost")
            time.sleep(0.5)
            self.reset()
            # Decrease score
            scoreboard.decrease()

    def wall_collision(self, wall_group, scoreboard):
        for brick in wall_group:
            if self.corner.colliderect(brick.corner):
                # The difference between y position of ball and brick is usually < 3 px
                if abs(self.corner.midbottom[1] - brick.corner.midtop[1]) < 3 or abs(self.corner.midtop[1] - brick.corner.midbottom[1]) < 3:
                    print(f"Ball bottom: {self.corner.midbottom[1]}")
                    print(f"Brick top: {brick.corner.midtop[1]}")
                    print(f"Ball top: {self.corner.midtop[1]}")
                    print(f"Brick bottom: {brick.corner.midbottom[1]}")
                    print(f"Direction: {self.direction_y}")
                    print("--------------------------------------------------")
                    brick.kill()
                    self.wall_bounce()
                    # Increase score
                    scoreboard.increase()
                    # BREAK is necessary to stop two bricks being destroyed at one impact
                    # - otherwise ball continues in the original direction and destroys 3 bricks
                    # - because y position reverses twice when hitting two bricks at the same time
                    # - changes in y negate and ball continues in the original direction
                    break
                # Side was hit
                else:
                    # Condition against stuck in the wall bug
                    if self.corner.left > 5 and self.corner.right < GAME_WIDTH:
                        brick.kill()
                        self.direction_x *= -1
                        self.speed_increase()
                        # Play sound
                        self.bounce_sound()
                        # Increase score
                        scoreboard.increase()
                        break

    def paddle_collision(self, paddle):
        if self.corner.colliderect(paddle.corner):
            # When the ball hits paddle in the middle
            if abs(self.corner.midbottom[0] - paddle.corner.midtop[0]) < self.MID_THRESHOLD and self.direction_y > 0:
                # print("Hit centre")
                self.direction_y *= - 1
                # If the paddle is moving the same direction as the ball
                if (self.direction_x > 0 < paddle.direction) or (self.direction_x < 0 > paddle.direction):
                    if self.speed < MAX_SPEED:
                        self.speed += SPEED_INCREMENT
                        # print(f"Paddle direction: {paddle.direction}")
                        # print(f"Ball direction_x: {self.direction_x}")
                # If paddle and ball are moving opposite directions
                elif (self.direction_x > 0 > paddle.direction) or (self.direction_x < 0 < paddle.direction):
                    if self.speed > 2:
                        self.speed += SPEED_INCREMENT
                        # print(f"Paddle direction: {paddle.direction}")
                        # print(f"Ball direction_x: {self.direction_x}")
                # Play sound
                self.bounce_sound_2()
            else:
                # Ball has to go down, otherwise might get stuck in the paddle
                if self.direction_y > 0:
                    # When left edge of the paddle was hit
                    self.direction_y *= - 1

                    if abs(self.corner.midbottom[0] - paddle.corner.topleft[0]) < self.CORNER_THRESHOLD:
                        # If the paddle moves in the opposite direction to ball
                        if self.direction_x > 0 and paddle.direction == -1:
                            self.direction_x *= -1
                        # print("Hit left corner")
                    # When the right edge of the paddle was hit
                    elif abs(self.corner.midbottom[0] - paddle.corner.topright[0]) < self.CORNER_THRESHOLD:
                        # If the paddle moves in the opposite direction to ball
                        if self.direction_x < 0 and paddle.direction == 1:
                            self.direction_x *= -1
                        # print("Hit right corner")
                    # Play sound
                    self.bounce_sound_2()
            print(f"Ball speed: {self.speed}")

    def collision_detect(self, wall_group, paddle, scoreboard):
        # Handle border sides collisions
        self.border_collision(scoreboard)
        # Wall collision detection
        self.wall_collision(wall_group, scoreboard)
        # Paddle collision detection
        self.paddle_collision(paddle)
