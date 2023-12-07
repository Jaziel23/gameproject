import sys

import pygame

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Platformer Game')
        self.screen = pygame.display.set_mode((640, 480))

        self.clock = pygame.time.Clock()

        self.image = pygame.image.load('data\images\Characters\characters.png')

        self.image_pos = [160, 260]
        self.movement = [False, False]
   
    def run(self):
        while True:
            self.screen.blit(self.image, self.image_pos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # allow the user to quit
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.movement[0] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.movement[0] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = False
            pygame.display.update()
            self.clock.tick(60)

Game().run()
