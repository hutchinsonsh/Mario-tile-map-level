import pygame
import os
from pygame.sprite import Sprite

class Player(Sprite):
    def __init__(self, game, sb, x, y, settings, screen, ai_settings):
        super(Player, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.sb = sb
        self.game = game
        self.image = pygame.Surface((settings.tileSize, settings.tileSize))
        self.image.fill(self.ai_settings.red)
        self.rect = self.image.get_rect()
        self.x = x * settings.tileSize
        self.y = y * settings.tileSize

        self.rect.x = self.x
        self.rect.y = self.y

        # for finding the edges of the player rect
        self.leftEdge = self.rect.x
        self.rightEdge = self.rect.x + settings.tileSize
        self.topEdge = self.rect.y
        self.bottomEdge = self.rect.y + settings.tileSize

        # for moving right/if user is pressing on a key
        self.movingRight = False
        self.movingLeft = False
        self.movingUp = False
        self.movingDown = False

        # if collision, by how much can user move
        self.rightV = ai_settings.playerSpeed
        self.leftV = ai_settings.playerSpeed

        # this makes sense to have in my head
        self.canMoveRight = True
        self.canMoveLeft = True
        self.canMoveUp = True
        self.canMoveDown = True

        self.jumpCount = 0
        self.jumping = False
        self.miniJumpCount = 0      # for when user hits a mystery box
        self.miniJumping = False

        self.fallCount = 0
        self.falling = False

        # for automatic movement when player reaches end flag
        self.stillMovingDown = True

    # updates movements (left/right, up/down)- confusing but I can't think of a way to refactor it
    def update(self, settings, wall):
        # user can't control movements during flag scene
        if not settings.endingMovements:
            # for moving right
            if self.movingRight and self.canMoveRight:
                self.rect.x += self.rightV
                self.leftEdge = self.rect.x
                self.rightEdge = self.rect.x + self.ai_settings.tileSize

            # for moving left
            if self.movingLeft and self.canMoveLeft:
                self.rect.x -= self.leftV
                self.leftEdge = self.rect.x
                self.rightEdge = self.rect.x + self.ai_settings.tileSize

            # for the jumping part
            if self.movingUp and not self.jumping and not self.falling:
                self.canMoveDown = True
                self.jumping = True

            # for the falling part
            if self.movingDown and self.canMoveDown:
                self.jumping = False
                self.falling = True

            # for the mini jump
            if self.miniJumping:
                self.rect.y -= self.ai_settings.playerMiniJumping[self.miniJumpCount]
                if self.miniJumpCount > 22:
                    self.miniJumping = False
                    self.miniJumpCount = 0
                else:
                    self.miniJumpCount += 1

            # jumping part 2
            self.jumpingMethod(settings, wall)

            # for checking if player is falling(anytime they are not jumping or on the ground)
            self.fallingMethod(settings, wall)

            # updates any changes
            self.topEdge = self.rect.y
            self.bottomEdge = self.rect.y + self.ai_settings.tileSize

        # for automatic movements at end
        if settings.endingMovements:
            self.flagEndScene(settings, wall)

    def fallingMethod(self, settings, wall):
        if self.falling and self.canMoveDown:
            num = self.ai_settings.playerFalling[self.fallCount]
            tempNum = 10
            if self.movingDown:
                num += 5
            for x in wall:
                if x.topEdge >= self.bottomEdge and x.topEdge - self.bottomEdge <= num:
                    if (x.leftEdge < self.leftEdge < x.rightEdge) or (x.leftEdge < self.rightEdge < x.rightEdge) or \
                            (x.leftEdge == self.leftEdge and x.rightEdge == self.rightEdge):
                        if x.type != '6':
                            tempNum = x.topEdge - self.bottomEdge
                        else:
                            self.sb.addScore(50)
                            self.game.mapName.updateMap('coin', x.x, x.y)
                            wall.remove(x)
                            self.sb.collectCoin(1)
                        if x.type == 'm' and self.game.mapName != self.game.map4 and \
                                self.game.mapName != self.game.map5 and self.movingDown:
                            self.canMoveDown = False
                            self.falling = False
                            self.miniJumping = True
                            self.sb.collectCoin(10)
                            self.sb.addScore(100)
                            x.type = 'c'
                            x.moving = True
                            self.game.mapName.updateMap('m', x.x, x.y)
                        elif x.type == 'm' and (self.game.mapName == self.game.map4 or \
                                                self.game.mapName == self.game.map5) and self.movingDown:
                            self.canMoveDown = False
                            self.falling = False
                            self.miniJumping = True
                            x.type = 'c'
                            x.moving = True
                            self.game.mapName.updateMap('m', x.x, x.y)
            if not self.canMoveDown:
                self.movingDown = False
            else:
                if tempNum <= num:
                    self.rect.y += tempNum
                    self.falling = False
                    self.movingDown = False
                    self.fallCount = 0
                else:
                    self.rect.y += num
                    self.fallCount += 1

    def jumpingMethod(self, settings, wall):
        if self.jumping:
            num = self.ai_settings.playerJumping[self.jumpCount]
            tempNum = 10
            for x in wall:
                if self.topEdge >= x.bottomEdge and self.topEdge - x.bottomEdge <= num:
                    if (x.leftEdge < self.leftEdge < x.rightEdge) or (x.leftEdge < self.rightEdge < x.rightEdge) or \
                            (x.leftEdge == self.leftEdge and x.rightEdge == self.rightEdge):
                        tempNum = self.topEdge - x.bottomEdge
                        # if user hits a mystery box while jumping
                        if x.type == 'm' and self.game.mapName != self.game.map4 and self.game.mapName != self.game.map5:
                            self.sb.collectCoin(10)
                            self.sb.addScore(100)
                            x.type = 'c'
                            x.moving = True
                            x.hitUp = True
                            self.game.mapName.updateMap('m', x.x, x.y)
                        elif x.type == 'm' and (self.game.mapName == self.game.map4 or \
                                                self.game.mapName == self.game.map5):
                            x.type = 'c'
                            x.moving = True
                            x.hitUp = True
                            self.game.mapName.updateMap('m', x.x, x.y)
            if tempNum < num:
                self.rect.y -= tempNum
                self.jumping = False
                self.jumpCount = 0
            else:
                self.rect.y -= self.ai_settings.playerJumping[self.jumpCount]
            if self.jumpCount > 46 or self.falling:
                self.jumping = False
                self.jumpCount = 0
            else:
                self.jumpCount += 1

        if not self.jumping:
            self.jumpCount = 0

    def flagEndScene(self, settings, wall):
        if self.stillMovingDown:
            for x in wall:
                if x.topEdge >= self.bottomEdge and x.topEdge - self.bottomEdge < 2:
                    if (x.leftEdge < self.leftEdge < x.rightEdge) or (x.leftEdge < self.rightEdge < x.rightEdge) or \
                            (x.leftEdge == self.leftEdge and x.rightEdge == self.rightEdge):
                        self.rect.y += x.topEdge - self.bottomEdge
                        self.topEdge = self.rect.y
                        self.bottomEdge = self.rect.y + self.ai_settings.tileSize
                        self.stillMovingDown = False
        if self.stillMovingDown:
            self.rect.y += 2
            self.topEdge = self.rect.y
            self.bottomEdge = self.rect.y + self.ai_settings.tileSize

        else:
            self.canMoveRight = True
            for x in wall:
                if x.type != 'E':
                    if x.leftEdge >= self.leftEdge and x.leftEdge - self.leftEdge < 2:
                        if (x.bottomEdge == self.bottomEdge and x.topEdge == self.topEdge):
                            self.rect.x += x.leftEdge - self.leftEdge
                            self.leftEdge = self.rect.x
                            self.rightEdge = self.rect.x + self.ai_settings.tileSize
                            self.canMoveRight = False
                            self.game.playing = False
                            settings.endingMovements = False
            if self.canMoveRight:
                self.rect.x += 2
                self.leftEdge = self.rect.x
                self.rightEdge = self.rect.x + self.ai_settings.tileSize

    # sets image to the right position
    def draw(self, screen):
        self.screen.blit(self.image, self.rect)
        
