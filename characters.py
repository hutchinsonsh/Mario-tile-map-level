import pygame
import os
import random
from pygame.sprite import Sprite

class Characters(Sprite):
    def __init__(self, game, x, y, settings, type):
        super(Characters, self).__init__()
        self.settings = settings
        self.game = game
        self.type = type
        # determining how big the surface of the image is

        self.image = pygame.Surface((settings.tileSize * 2, settings.tileSize * 2))

        # determining if 'wall', 'jump block', 'border' or 'goomba'
        self.image = pygame.image.load(os.path.join('images', 'goomba.png'))
        self.image = pygame.transform.scale(self.image, (64, 64))

        self.rect = self.image.get_rect()
        self.x = x * self.settings.tileSize
        self.y = y * self.settings.tileSize

        self.rect.x = self.x
        self.rect.y = self.y

        self.leftEdge = self.rect.x
        self.rightEdge = self.rect.x + (self.settings.tileSize * 2)
        self.topEdge = self.rect.y
        self.bottomEdge = self.rect.y + (self.settings.tileSize * 2)

        # for determing whether the goomba starts off walking left or right
        leftRight = random.randrange(0, 2)
        if leftRight == 0:
            self.goingRight = True
            self.goingLeft = False
        else:
            self.goingRight = False
            self.goingLeft = True

    # moves the goomba over one space each iteration
    def moveChar(self):
        if self.goingRight:
            self.rect.x += 1
            self.leftEdge = self.rect.x
            self.rightEdge = self.rect.x + (self.settings.tileSize * 2)
        elif self.goingLeft:
            self.rect.x -= 1
            self.leftEdge = self.rect.x
            self.rightEdge = self.rect.x + (self.settings.tileSize * 2)

    # if goomba hits wall- changes direction
    def switch(self):
        if self.goingRight:
            self.goingRight = False
            self.goingLeft = True
        elif self.goingLeft:
            self.goingRight = True
            self.goingLeft = False

    # draws everything
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    # updates everything
    def update(self, camera):
        self.x *= camera.width
        self.y *= camera.height

class Coins(Sprite):
    def __init__(self, game, x, y, settings, type):
        super(Coins, self).__init__()
        self.settings = settings
        self.game = game
        self.type = type
        self.image = pygame.image.load(os.path.join('images', 'coin.png'))
        self.image = pygame.transform.scale(self.image, (32, 32))

        self.rect = self.image.get_rect()
        self.x = x * settings.tileSize
        self.y = y * settings.tileSize

        self.rect.x = self.x
        self.rect.y = self.y

        self.leftEdge = x * settings.tileSize
        self.bottomEdge = (y + 1) * settings.tileSize
        self.rightEdge = (x + 1) * settings.tileSize
        self.topEdge = y * settings.tileSize

    # draws everything
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    # updates everything
    def update(self, camera):
        self.x *= camera.width
        self.y *= camera.height
        
