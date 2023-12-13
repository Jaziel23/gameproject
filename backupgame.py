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

# Background images
background_images = [
    pygame.image.load('Platformer/data/images/Characters/Free/Background/parallax-mountain-bg.png'),
    pygame.image.load('Platformer\data\images\Characters\Free\Background\parallax-mountain-mountains.png'),
    pygame.image.load('Platformer\data\images\Characters\Free\Background\parallax-mountain-foreground-trees.png'),
    pygame.image.load('Platformer\data\images\Characters\Free\Background\parallax-mountain-trees.png'),
    pygame.image.load('Platformer\data\images\Characters\Free\Background\parallax-mountain-montain-far.png')
]

backgrounds = [pygame.transform.scale(image, (WIDTH, HEIGHT)) for image in background_images]
background_speeds = [1, 2, 3, 4, 5]  # Adjust these speeds as needed

# Plane image
plane_image = pygame.image.load('Platformer\data\images\Characters\plane_3_blue.png')
plane_image = pygame.transform.scale(plane_image, (50, 35))  # Adjust the size as needed

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Set up the game clock
clock = pygame.time.Clock()

# Game variables
plane_x = 50
plane_y = HEIGHT // 2
plane_speed = 5
jumping = False
jump_duration = 0.3
jump_timer = 0.3
jump_speed = 50
gravity = 3

pipes = []

# Score variables
score = 0
font = pygame.font.Font(None, 36)
score_update_frequency = 1

def draw_background():
    for i, background in enumerate(backgrounds):
        offset = -(frame_count * background_speeds[i]) % background.get_width()
        screen.blit(background, (offset - background.get_width(), 0))
        screen.blit(background, (offset, 0))

def draw_ground():
    pygame.draw.rect(screen, BLACK, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

def draw_plane(x, y):
    screen.blit(plane_image, (x, y))

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
frame_count = 0
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
        plane_y -= jump_timer * jump_speed
        jump_timer -= dt

        if jump_timer <= 0:
            jumping = False

    plane_y += gravity

    for pipe in pipes:
        pipe[0] -= plane_speed

        if plane_x < pipe[0] + PIPE_WIDTH and \
                plane_x + plane_image.get_width() > pipe[0] and \
                (plane_y < pipe[1] or plane_y + plane_image.get_height() > HEIGHT - pipe[2]):
            game_over()

        if pipe[0] < -PIPE_WIDTH:
            pipes.remove(pipe)

    if frame_count % 90 == 0:
        top_pipe_height = random.randint(50, HEIGHT // 2 - 50)
        bottom_pipe_height = HEIGHT - top_pipe_height - 150
        pipes.append([WIDTH, top_pipe_height, bottom_pipe_height])

    if frame_count % score_update_frequency == 0:
        score += 1

    draw_background()
    draw_ground()
    draw_plane(plane_x, plane_y)

    for pipe in pipes:
        draw_pipe(pipe[0], pipe[1], pipe[2])

    draw_score(score)

    pygame.display.flip()
