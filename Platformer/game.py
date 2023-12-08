#download pygame first!!

import pygame

import sys

pygame.init()

#setup display and its name
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Platformer")

#sets colors
white = (255, 255, 255)
black = (0, 0, 0)

#player setup
player_size = 50
player_x = width // 2 - player_size // 2
player_y = height - player_size * 2
player_speed = 5
is_jumping = False
jump_count = 10

#game loop

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    keys = pygame.key.get_pressed()
    # move player
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < width - player_size:
        player_x += player_speed
 # jumping mechanics
    if not is_jumping:
        if keys[pygame.K_SPACE]:
            is_jumping = True
    else:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            player_y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            is_jumping = False
            jump_count = 10

    # draw background
    screen.fill(white)

    # draw player
    pygame.draw.rect(screen, black, (player_x, player_y, player_size, player_size))

    # Update display
    pygame.display.flip()

    # sets frame rate
    pygame.time.Clock().tick(30)