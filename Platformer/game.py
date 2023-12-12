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
PLAYER_SIZE = 200  # Increase the size of the player
PLATFORM_WIDTH = WIDTH
PLATFORM_HEIGHT = 40  # Increase the height of the platform

# Load character frames
idle_frame_filenames = ["Tile000.png", "Tile001.png", "Tile002.png", "Tile003.png"]  # Idle frames
walk_frame_filenames = ["Tile000.png", "Tile001.png", "Tile002.png", "Tile003.png"]  # Walking frames
idle_frames = [pygame.image.load(os.path.join("Platformer", "data", "images", "Characters", "Enemy", "idle", filename)) for filename in idle_frame_filenames]
walk_frames = [pygame.image.load(os.path.join("Platformer", "data", "images", "Characters", "Enemy", "walk", filename)) for filename in walk_frame_filenames]

# Load the new background image
new_background_image = pygame.image.load(os.path.join("Platformer", "data", "images", "Characters", "Free", "Background", "parallax-mountain-bg.png"))
new_background_image = pygame.transform.scale(new_background_image, (WIDTH, HEIGHT))

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Platformer")
clock = pygame.time.Clock()

# Player
player = pygame.Rect(WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT // 2 - PLAYER_SIZE // 2, PLAYER_SIZE, PLAYER_SIZE)
player_speed = 5
player_jump = -15  # Adjust jump height (more negative means higher jump)
is_jumping = False
jump_count = 10  # Adjust the number of frames the jump lasts

# Platforms
platforms = [pygame.Rect(0, HEIGHT - 40, WIDTH, PLATFORM_HEIGHT)]  # Temporary tiles at the bottom

# Animation parameters
num_idle_frames = len(idle_frames)
current_idle_frame = 0
idle_animation_speed = 0.1
idle_animation_timer = 0

num_walk_frames = len(walk_frames)
current_walk_frame = 0
walk_animation_speed = 0.1
walk_animation_timer = 0

# Direction the player is facing (1 for right, -1 for left)
player_direction = 1

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Idle animation logic
    idle_animation_timer += clock.get_time() / 1000.0
    if idle_animation_timer >= idle_animation_speed:
        idle_animation_timer = 0
        current_idle_frame = (current_idle_frame + 1) % num_idle_frames

    # Walk animation logic
    walk_animation_timer += clock.get_time() / 1000.0
    if walk_animation_timer >= walk_animation_speed and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
        walk_animation_timer = 0
        current_walk_frame = (current_walk_frame + 1) % num_walk_frames

    # Jumping logic
    if not is_jumping:
        if keys[pygame.K_SPACE]:
            is_jumping = True
            jump_count = 10  # Reset jump count when starting to jump
    else:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            player.y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            is_jumping = False

    # Apply gravity only when not jumping
    if not is_jumping and player.y < HEIGHT - PLAYER_SIZE:
        player.y += 5
    elif not is_jumping:
        player.y = HEIGHT - PLAYER_SIZE  # Ensure the player stays within the screen when falling

    # Move player
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
        player_direction = -1  # Set direction to left
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += player_speed
        player_direction = 1  # Set direction to right

    # Check for collisions with platforms
    for platform in platforms:
        if player.colliderect(platform):
            player_bottom = player.y + PLAYER_SIZE
            platform_top = platform.y
            if player_bottom < platform_top:
                player.y = platform_top - PLAYER_SIZE
                is_jumping = False
                jump_count = 10  # Reset jump count when landing
            else:
                player.y = platform.y + PLATFORM_HEIGHT

    # Adjust player position to prevent floating and ensure the player stays on the screen
    player_bottom = player.y + PLAYER_SIZE
    platform_top = platforms[0].y  # Assuming there is only one platform
    if player_bottom < platform_top:
        player.y = platform_top - PLAYER_SIZE

    player.y = max(0, min(player.y, HEIGHT - PLAYER_SIZE))

    # Update the display
    screen.blit(new_background_image, (0, 0))

    # Draw the player animation with direction
    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
        player_image = pygame.transform.scale(walk_frames[current_walk_frame], (PLAYER_SIZE, PLAYER_SIZE))
    else:
        player_image = pygame.transform.scale(idle_frames[current_idle_frame], (PLAYER_SIZE, PLAYER_SIZE))

    if player_direction == -1:
        player_image = pygame.transform.flip(player_image, True, False)  # Flip horizontally for left direction

    # Draw the player
    screen.blit(player_image, (player.x, player.y))

    # Draw the platforms in brown color
    for platform in platforms:
        pygame.draw.rect(screen, (139, 69, 19), platform)

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
