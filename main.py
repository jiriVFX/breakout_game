import pygame
from constants import *
from paddle import Paddle
from brick import Brick
from ball import Ball
import time

# from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT)

# Initialize pygame
pygame.init()

# ----------------------------------------------------------------------------------------------------------------------

# Create screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Breakout game")
# Set background colour
screen.fill(white)

# Font
pygame.font.init()
font = pygame.font.SysFont("Consolas", 60, bold=True)
text_won = font.render("You won!", True, white)
text_won_corner = text_won.get_rect(center=((GAME_WIDTH) / 2, GAME_HEIGHT / 2 - 40))
#pygame.draw.rect(text_surface_won, yellow, rect, 1)

# Gaming area surface
game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
game_surface.fill(dark_grey)
# rect = game_space.get_rect()

# Create paddle
paddle = Paddle(PADDLE_WIDTH, PADDLE_HEIGHT, red)
# Create ball
# ball = Ball(, blue)

# Create ball
ball = Ball(20, white)

# Create wall
wall = pygame.sprite.Group()
# Create wall of bricks
for i in range(5):
    colour = None
    if i == 0:
        colour = red
    elif i == 1:
        colour = orange
    elif i == 2:
        colour = yellow
    elif i == 3:
        colour = green
    else:
        colour = blue
    # Create one line of bricks
    for j in range(0, 10):
        # Each brick's starting position is
        # x = (j * size of the brick + half the size of the brick + offset from the left)
        # y = i * (height of the brick + space between lines) + offset from the top
        # print(colour)
        wall.add(Brick((j * GAME_WIDTH / 10 + GAME_WIDTH / 10 / 2 + 5), i * (GAME_HEIGHT / 30 + 5) + 60, colour))
# ----------------------------------------------------------------------------------------------------------------------

# Game loop
clock = pygame.time.Clock()
game_on = True
one_time = 0
while game_on:
    # Quit the game when X is clicked to close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_on = False
            else:
                print(pygame.key.name(event.key))

    # Ball collision detection and movement ----------------------------------------------------------------------------

    ball.move()

    # Collision detection and bouncing
    ball.collision_detect(wall, paddle)

    # Pressed down keys boolean list - 0 for keys not pressed and 1 for keys pressed
    pressed_keys = pygame.key.get_pressed()
    # Move the paddle
    paddle.move(pressed_keys)

    # Rendering --------------------------------------------------------------------------------------------------------

    # Place the gaming area on the screen
    screen.blit(game_surface, (5, 5))

    # Render all the bricks in the wall
    for brick in wall:
        # print(brick.corner)
        screen.blit(brick.surface, brick.corner)

    # Place the paddle on the screen
    # Places paddle in the middle + paddle corner(rect) position (changes when paddle moves)
    screen.blit(paddle.surface, paddle.corner)
    # Place the ball on the screen
    screen.blit(ball.surface, ball.corner)
    # print(paddle.corner)
    # screen.blit(paddle.surface, ((GAME_WIDTH - PADDLE_WIDTH) / 2, GAME_HEIGHT - 40))

    # Check whether there are any bricks left
    # Render End Game text - has to be the last to render, otherwise covered by other surfaces
    if not wall:
        screen.blit(text_won, text_won_corner)
        pygame.display.update()
        # Wait for x miliseconds until closing the game
        pygame.time.delay(2000)
        game_on = False

    # Refresh display
    pygame.display.flip()

    # Set refresh rate to 60 times per second
    clock.tick(60)
    # print(clock.get_fps())

pygame.quit()
