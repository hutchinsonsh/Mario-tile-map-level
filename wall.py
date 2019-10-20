import pygame
import os
from pygame.sprite import Sprite

class Wall(Sprite):
    def __init__(self, game, x, y, settings, type):
        super(Wall, self).__init__()
        self.settings = settings
        self.g = game
        self.type = type
        self.image = pygame.Surface((settings.tileSize, settings.tileSize))

        self.rect = self.image.get_rect()
        self.x = x * settings.tileSize
        self.y = y * settings.tileSize

        self.rect.x = self.x
        self.rect.y = self.y

        self.leftEdge = x * settings.tileSize
        self.bottomEdge = (y + 1) * settings.tileSize
        self.rightEdge = (x + 1) * settings.tileSize
        self.topEdge = y * settings.tileSize

        # for moving the m boxes when they're hit
        self.movingBack = 0
        self.hitUp = False
        self.cycle = 0
        self.moveBack = 0

        # 1 = ground, 2 = border, 3 = jump block, 7 = pipe
        # b = hit block; m = mystery box;
        # n = used box; E = flag; T= end castle; d = door to end castle

        self.determineType()

    # what obj is being created based on what map I am on
    def determineType(self):
        if self.g.mapName == self.g.map1 or self.g.mapName == self.g.map3:
            if self.type == '1':
                self.image = pygame.image.load(os.path.join('images', 'block.jpg'))
                self.image = pygame.transform.scale(self.image, (32, 32))
            elif self.type == '3':
                self.image = pygame.image.load(os.path.join('images', 'jump.png'))
                self.image = pygame.transform.scale(self.image, (32, 32))
            elif self.type == '2' or self.type == 'l':
                self.image.fill(self.settings.blue)
            elif self.type == 'b':
                self.image = pygame.image.load(os.path.join('images', 'hitBlock.png'))
                self.image = pygame.transform.scale(self.image, (32, 32))
            elif self.type == 'm':
                self.image = pygame.image.load(os.path.join('images', 'questionMark.png'))
                self.image = pygame.transform.scale(self.image, (32, 32))
            elif self.type == 'n':
                self.image = pygame.image.load(os.path.join('images', 'emptyBlock.png'))
                self.image = pygame.transform.scale(self.image, (32, 32))
            elif self.type == 'E':
                self.image = pygame.image.load(os.path.join('images', 'endFlag.png'))
                self.image = pygame.transform.scale(self.image, (64, 384))
                self.leftEdge = self.rect.x + (self.settings.tileSize * 1.5) - 4
                self.rightEdge = self.rect.x + (self.settings.tileSize * 2)
                self.topEdge = self.rect.y
                self.bottomEdge = self.rect.y + (self.settings.tileSize * 12)
            elif self.type == 'T':
                self.image = pygame.image.load(os.path.join('images', 'endCastle.png'))
                self.image = pygame.transform.scale(self.image, (160, 160))
                self.leftEdge = self.rect.x
                self.rightEdge = self.rect.x + (self.settings.tileSize * 5)
                self.topEdge = self.rect.y
                self.bottomEdge = self.rect.y + (self.settings.tileSize * 5)
            elif self.type == 'd':
                self.image.fill(self.settings.black)

            # for the pipe
            elif self.type == '7':
                self.image = pygame.image.load(os.path.join('images', 'pipe.png'))
                self.image = pygame.transform.scale(self.image, (96, 64))

                self.leftEdge = self.rect.x
                self.rightEdge = self.rect.x + (self.settings.tileSize * 3)
                self.topEdge = self.rect.y
                self.bottomEdge = self.rect.y + (self.settings.tileSize * 2)

        elif self.g.mapName == self.g.map2:
            if self.type == '1':
                self.image = pygame.image.load(os.path.join('images', 'underGroundBlock.png'))
                self.image = pygame.transform.scale(self.image, (32, 32))
            elif self.type == '3':
                self.image = pygame.image.load(os.path.join('images', 'undergroundJump.png'))
                self.image = pygame.transform.scale(self.image, (32, 32))
            elif self.type == '2' or self.type == 'l':
                self.image.fill(self.settings.black)
            elif self.type == 'b':
                self.image = pygame.image.load(os.path.join('images', 'underGroundHitBlock.png'))
                self.image = pygame.transform.scale(self.image, (32, 32))
            elif self.type == 'm':
                self.image = pygame.image.load(os.path.join('images', 'questionMark.png'))
                self.image = pygame.transform.scale(self.image, (32, 32))
            elif self.type == 'n':
                self.image = pygame.image.load(os.path.join('images', 'emptyBlock.png'))
                self.image = pygame.transform.scale(self.image, (32, 32))

            if self.type == '7':
                self.image = pygame.image.load(os.path.join('images', 'pipe.png'))
                self.image = pygame.transform.scale(self.image, (96, 64))

                self.leftEdge = self.rect.x
                self.rightEdge = self.rect.x + (self.settings.tileSize * 3)
                self.topEdge = self.rect.y
                self.bottomEdge = self.rect.y + (self.settings.tileSize * 2)

        elif self.g.mapName == self.g.map4:
            if self.type == '1':
                self.image.fill(self.settings.blue)
            elif self.type == '2':
                self.image.fill(self.settings.grey)
            elif self.type == 'm':
                self.image = pygame.image.load(os.path.join('images', 'questionMark.png'))
                self.image = pygame.transform.scale(self.image, (32, 32))

        elif self.g.mapName == self.g.map5:
            if self.type == '2':
                self.image = pygame.image.load(os.path.join('images', 'block.jpg'))
                self.image = pygame.transform.scale(self.image, (32, 32))
            elif self.type == 'm':
                self.image = pygame.image.load(os.path.join('images', 'questionMark.png'))
                self.image = pygame.transform.scale(self.image, (32, 32))

    # changes image of a wall
    def changeImage(self):
        # for when mystery box is hit- changes to used box
        if self.type == 'n':
            self.image = pygame.image.load(os.path.join('images', 'emptyBlock.png'))
            self.image = pygame.transform.scale(self.image, (32, 32))
        elif self.type == 'E':
            self.image = pygame.image.load(os.path.join('images', 'endFlagHit.png'))

    # draws everything
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    # updates walls
    def update(self, camera):
        # moves mystery box up/down when hit
        if self.type == 'c':
            self.moving = True
            if self.moving == True:
                # for determing whether box moves up or down
                if self.hitUp == True:
                    if self.cycle % 2 == 0:
                        self.rect.y -= 1
                        self.topEdge = self.rect.y
                        self.bottomEdge = self.rect.y + self.settings.tileSize
                else:
                    if self.cycle % 2 == 0:
                        self.rect.y += 1
                        self.topEdge = self.rect.y
                        self.bottomEdge = self.rect.y + self.settings.tileSize
                self.cycle += 2;
                if self.cycle == 20:
                    self.cycle = 0
                    self.moveBack += 1

                # for making sure the box moves both up/down or down/up
                    if self.hitUp == True:
                        self.hitUp = False
                    else:
                        self.hitUp = True
                if self.moveBack > 1:
                    self.type = 'n'
                    self.moving = False
                    self.moveBack = 0
                    self.g.mapName.updateMap('c', self.rect.x, self.rect.y)
                    self.changeImage()
                    # for gameOver screen- if player hits box- restarts game
                    if self.g.mapName == self.g.map4:
                        self.g.playerRestarts = True
                    # for endScreen- if player hits left box- restarts game
                    elif self.g.mapName == self.g.map5 and self.rect.x < 500:
                        self.g.playerRestarts = True
                    # for endScreen- if player hits left box- quits game
                    elif self.g.mapName == self.g.map5 and self.rect.x > 500:
                        self.g.playerRestarts = False
                        self.g.playerDone = True
                        self.g.running = False



        self.x *= camera.width
        self.y *= camera.height
        
