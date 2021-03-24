import pygame
from constants import *
from paddle import Paddle
from brick import Brick
from ball import Ball
from scoreboard import Scoreboard
import time

# Initialize pygame
pygame.init()

# ----------------------------------------------------------------------------------------------------------------------

# Create screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Breakout game")
# Set background colour
screen.fill(white)

# Scoreboard
scoreboard = Scoreboard()

# Font
pygame.font.init()
font = pygame.font.SysFont("Consolas", 60, bold=True)
text_won = font.render("You won!", True, white)
text_won_corner = text_won.get_rect(center=((GAME_WIDTH) / 2, GAME_HEIGHT / 2 - 40))

# Sounds
collision_sound = pygame.mixer.Sound("static/sound/bat_hit.mp3")
winning_sound = pygame.mixer.Sound("static/sound/chime.mp3")

# Gaming area surface
game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
game_surface.fill(dark_grey)
# rect = game_space.get_rect()

# Create paddle
# paddle = Paddle(PADDLE_WIDTH, PADDLE_HEIGHT, red)
paddle = Paddle("static/img/paddle.png")

# Create ball
#ball = Ball(20, white)
ball = Ball("static/img/ball.png")

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
        wall.add(Brick((j * GAME_WIDTH // 10 + GAME_WIDTH // 10 // 2 + 5), i * (GAME_HEIGHT // 20 + 5) + 80, colour))
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

    # Ball collision detection and movement ----------------------------------------------------------------------------

    ball.move()

    # Collision detection and bouncing
    ball.collision_detect(wall, paddle, scoreboard)

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

    # Place scoreboard on the screen
    screen.blit(scoreboard.score_text, scoreboard.corner)

    # Check whether there are any bricks left
    # Render End Game text - has to be the last to render, otherwise covered by other surfaces
    if not wall:
        # Play winning sound
        winning_sound.play()
        screen.blit(text_won, text_won_corner)
        pygame.display.update()
        # Wait for x miliseconds until closing the game
        pygame.time.delay(3000)
        game_on = False

    # Refresh display
    pygame.display.flip()

    # Set refresh rate to 60 times per second
    clock.tick(60)
    # print(clock.get_fps())

# Quit all the sounds and the game
pygame.mixer.quit()
pygame.quit()
