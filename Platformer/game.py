import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_SIZE = 70  # Increase the size of the player
PLATFORM_WIDTH = WIDTH
PLATFORM_HEIGHT = 20

# Set the correct path to your image directory
image_dir = os.path.join("Platformer", "data", "images", "Characters")

# Load character and background images
player_image = pygame.image.load(os.path.join(image_dir, "characters1.png"))
background_image = pygame.image.load(os.path.join(image_dir, "Free", "Background", "Blue.png"))
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Platformer")
clock = pygame.time.Clock()

# Player
player = pygame.Rect(WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT // 2 - PLAYER_SIZE // 2, PLAYER_SIZE, PLAYER_SIZE)
player_speed = 5
player_jump = -15  # Adjust jump height (more negative means higher jump)
is_jumping = False

# Platforms
platforms = [pygame.Rect(0, HEIGHT - 20, PLATFORM_WIDTH, PLATFORM_HEIGHT)]

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Move player
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += player_speed

    # Jumping
    if not is_jumping:
        if keys[pygame.K_SPACE]:
            is_jumping = True
    else:
        player.y += player_jump
        if player.y >= HEIGHT - PLAYER_SIZE:
            is_jumping = False

    # Apply gravity
    if player.y < HEIGHT - PLAYER_SIZE:
        player.y += 5

    # Check for collisions with platforms
    for platform in platforms:
        if player.colliderect(platform) and not is_jumping:
            player.y = platform.y - PLAYER_SIZE
            is_jumping = False

    # Update the display
    screen.blit(background_image, (0, 0))

    # Draw the player image
    screen.blit(pygame.transform.scale(player_image, (PLAYER_SIZE, PLAYER_SIZE)), player.topleft)

    # Draw the platforms
    for platform in platforms:
        pygame.draw.rect(screen, WHITE, platform)

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
