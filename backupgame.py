import pygame
import sys
import random

pygame.init()
pygame.font.init()

# Constants
WIDTH, HEIGHT = 800, 600
GROUND_HEIGHT = 50
PIPE_WIDTH = 50
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Background image
original_background_image = pygame.image.load('Platformer/data/images/Characters/Free/Background/parallax-mountain-bg.png')
background_image = pygame.transform.scale(original_background_image, (WIDTH, HEIGHT))

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Set up the game clock
clock = pygame.time.Clock()

# Game variables
bird_x = 50
bird_y = HEIGHT // 2
bird_width = 30
bird_height = 30
bird_speed = 5
jumping = False
jump_duration = 0.3
jump_timer = 0.3
jump_speed = 50  # Adjusted the jump speed
gravity = 3

pipes = []

# Score variables
score = 0
font = pygame.font.Font(None, 36)
score_update_frequency = 1  # Update the score every 10 frames

def draw_ground():
    pygame.draw.rect(screen, BLACK, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

def draw_bird(x, y):
    pygame.draw.rect(screen, RED, (x, y, bird_width, bird_height))

def draw_pipe(x, top_height, bottom_height):
    pygame.draw.rect(screen, BLACK, (x, 0, PIPE_WIDTH, top_height))
    pygame.draw.rect(screen, BLACK, (x, HEIGHT - bottom_height, PIPE_WIDTH, bottom_height))

def draw_score(score):
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))

def game_over():
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, BLACK)
    screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 37))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

# Game loop
frame_count = 0  # Track the number of frames
while True:
    dt = clock.tick(FPS) / 1000  # Delta time in seconds
    frame_count += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and not jumping:
        jumping = True
        jump_timer = jump_duration

    if jumping:
        bird_y -= jump_timer * jump_speed
        jump_timer -= dt

        if jump_timer <= 0:
            jumping = False

    bird_y += gravity

    # Move pipes
    for pipe in pipes:
        pipe[0] -= bird_speed

        # Check for collision with the bird
        if bird_x < pipe[0] + PIPE_WIDTH and \
                bird_x + bird_width > pipe[0] and \
                (bird_y < pipe[1] or bird_y + bird_height > HEIGHT - pipe[2]):
            game_over()

        # Remove off-screen pipes
        if pipe[0] < -PIPE_WIDTH:
            pipes.remove(pipe)

    # Generate new pipes
    if frame_count % 90 == 0:
        top_pipe_height = random.randint(50, HEIGHT // 2 - 50)
        bottom_pipe_height = HEIGHT - top_pipe_height - 150  # Adjust the gap size as needed
        pipes.append([WIDTH, top_pipe_height, bottom_pipe_height])

    # Update score based on frames survived
    if frame_count % score_update_frequency == 0:
        score += 1

    # Draw the background
    screen.blit(background_image, (0, 0))

    # Draw other elements on top of the background
    draw_ground()
    draw_bird(bird_x, bird_y)

    for pipe in pipes:
        draw_pipe(pipe[0], pipe[1], pipe[2])

    # Draw the score
    draw_score(score)

    pygame.display.flip()

