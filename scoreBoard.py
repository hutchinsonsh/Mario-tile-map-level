import pygame.font
import os
from pygame.sprite import Group

class ScoreBoard():
    def __init__(self, g, ai_settings, screen):
        self.g = g
        self.ai_settings = ai_settings
        self.screen = screen

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.livesLeft = 3
        self.coinsCollected = 0
        self.score = 0

        self.image1 = pygame.image.load(os.path.join('images', 'coin.png'))
        self.image1 = pygame.transform.scale(self.image1, (32, 32))
        self.image2 = pygame.image.load(os.path.join('images', 'redBlock.png'))
        self.image2 = pygame.transform.scale(self.image2, (32, 32))


    # takes off a life/removes coins
    def lostALife(self):
        self.livesLeft -= 1
        if self.coinsCollected >= 10:
            self.coinsCollected -= 10
        else:
            self.coinsCollected = 0

    # for when player collects 100 coins- adds a life
    def gainALife(self):
        self.livesLeft += 1

    # adds a certain amount of coins to total collection
    def collectCoin(self, coin):
        self.coinsCollected += coin
        if self.coinsCollected > 100:
            self.coinsCollected -= 100
            self.gainALife()

    # adds a certain amount to the total score
    def addScore(self, score2):
        self.score += score2

    # displays livesLeft, coinsCollected, and total score
    def showScore(self, g):
        if g.mapName != g.map4 and g.mapName != g.map5:
            if g.mapName != g.map2:
                self.text = self.font.render(str(self.coinsCollected), 1, (0, 0, 0))
                self.text2 = self.font.render(str(self.livesLeft), 1, (0, 0, 0))
                self.text3 = self.font.render(str(self.score), 1, (0, 0, 0))
                self.text4 = self.font.render(str(g.minutes) + " : " + str(g.seconds), 1, (0, 0, 0))
            else:
                self.text = self.font.render(str(self.coinsCollected), 1, (255, 255, 255))
                self.text2 = self.font.render(str(self.livesLeft), 1,  (255, 255, 255))
                self.text3 = self.font.render(str(self.score), 1, (255, 255, 255))
                self.text4 = self.font.render(str(g.minutes) + " : " + str(g.seconds), 1, (255, 255, 255))

            self.screen.blit(self.text, (925, 25))
            self.screen.blit(self.image1, (890, 25))
            self.screen.blit(self.text2, (925, 65))
            self.screen.blit(self.image2, (890, 65))
            self.screen.blit(self.text3, (505, 25))
            self.screen.blit(self.text4, (50, 25))

        elif g.mapName == g.map5:
            self.text = self.font.render(str(self.coinsCollected), 1, (255, 255, 255))
            self.text2 = self.font.render(str(self.livesLeft), 1, (255, 255, 255))
            self.text3 = self.font.render(str(self.score), 1, (255, 255, 255))

            self.screen.blit(self.text3, (15*32, 250))
            self.screen.blit(self.text, (18*32, 300))
            self.screen.blit(self.image1, (13*32, 300))
            self.screen.blit(self.text2, (18*32, 350))
            self.screen.blit(self.image2, (13*32, 350))
            
