
import pygame
import sys
import random
pygame.init()
pygame.font.init()
# Constants
WIDTH, HEIGHT = 800, 300
GROUND_HEIGHT = 50
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("T-Rex Run")

# Set up the game clock
clock = pygame.time.Clock()

# Game variables
dino_x = 50
dino_y = HEIGHT - GROUND_HEIGHT - 60  # Adjusted initial position
dino_width = 30
dino_height = 30
dino_speed = 5
jumping = False
jump_duration = 0.5
jump_timer = 0
jump_speed = 20
gravity = 200

cactus_list = []

# Score variables
score = 0
font = pygame.font.Font(None, 36)

# Functions
def draw_ground():
    pygame.draw.rect(screen, BLACK, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

def draw_dino(x, y):
    pygame.draw.rect(screen, BLACK, (x, y, dino_width, dino_height))

def draw_cactus(x, y):
    pygame.draw.rect(screen, BLACK, (x, y, 20, 40))

def draw_score(score):
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))

def game_over():
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, WHITE)
    screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 37))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

# Game loop
while True:
    dt = clock.tick(FPS) / 1000  # Delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        jumping = True
        jump_timer = jump_duration

    if jumping:
        # Apply jump force based on timer
        dino_y -= jump_timer ** 2 * jump_speed
        jump_timer -= dt

        if jump_timer <= 0:
            jumping = False
            jump_timer = 0

    # Apply gravity when not jumping
    if not jumping and dino_y < HEIGHT - GROUND_HEIGHT - dino_height:
        dino_y += gravity * dt

    # Move cactus
    for cactus in cactus_list:
        cactus[0] -= dino_speed

        # Check for collision with the dinosaur
        if dino_x < cactus[0] + 20 and \
                dino_x + dino_width > cactus[0] and \
                dino_y < cactus[1] + 40 and \
                dino_y + dino_height > cactus[1]:
            game_over()

        # Remove off-screen cacti
        if cactus[0] < -20:
            cactus_list.remove(cactus)

    # Generate new cactus with reduced frequency
    if random.randint(0, 100) < 5:
        cactus_list.append([WIDTH, HEIGHT - GROUND_HEIGHT - 40])

    # Update score based on frames survived
    score += 1

    # Update screen
    screen.fill(WHITE)
    draw_ground()
    draw_dino(dino_x, dino_y)

    for cactus in cactus_list:
        draw_cactus(cactus[0], cactus[1])

    draw_score(score)

    pygame.display.flip()


