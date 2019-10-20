import sys
from pygame.locals import *
import gameFunction as gf
from pygame.sprite import Group
from scoreBoard import ScoreBoard
from settings import Settings
from tileMap import *
from characters import *

class Game:
    def __init__(self):
        # initializes game
        pygame.init()
        pygame.display.set_caption(settings.title)
        pygame.key.set_repeat(500, 100)
        self.seconds = 60
        self.minutes = 3
        pygame.time.set_timer(USEREVENT + 1, 1000)  # 1 second is 1000 milliseconds
        self.screen = pygame.display.set_mode((settings.w, settings.h))
        self.clock = pygame.time.Clock()
        self.sb = ScoreBoard(self, settings, self.screen)

        # for determning the map being used
        self.makeCopies()
        self.mapName = self.map1
        self.previousMapName = self.map1
        self.newMap = False
        self.new1()
        self.playerRestarts = False
        self.stillPlaying = True
        self.playerDone = False

        # for the timer
        self.clock = pygame.time.Clock()

    # takes the tile maps and converts them into arrays to read from
    def makeCopies(self):
        self.map1 = CopyMap("maps/copyMap.txt", settings)
        self.map2 = CopyMap("maps/copyUnderGroundMap.txt", settings)
        self.map3 = CopyMap("maps/copyMap2.txt", settings)
        self.map4 = CopyMap("maps/gameOver.txt", settings)
        self.map5 = CopyMap("maps/endScreen.txt", settings)

    # creates the tileMap/player locations/sets up camera
    def new1(self):
        self.wallGroup = Group()
        for row, tiles in enumerate(self.mapName.data):
            for col, tile in enumerate(tiles):
                gf.findWhichType(self, self.sb, tile, col, row, settings)
        self.camera = Camera(self.mapName.width, self.mapName.height, settings)

    # loads a new map if player reaches end of first map
    def new(self):
        for x in self.wallGroup:
            gf.findWhichMap(self, x, self.sb)
        if self.newMap:
            self.new1()
            self.newMap = False

    # draws the walls, characters, and player
    def draw(self, settings):
        if self.mapName != self.map4 and self.mapName != self.map2:
            self.screen.fill(settings.blue)
        else:
            self.screen.fill(settings.black)
        for x in self.wallGroup:
            self.screen.blit(x.image, self.camera.apply(x))
        self.screen.blit(self.newPlayer.image, self.camera.apply(self.newPlayer))
        self.sb.showScore(self)
        pygame.display.flip()

    # checks events, updates any changes, draws events/changes
    # where the main game is ran- only stops if player finishes or loses
    def run(self, settings):
        self.playing = True
        settings.endingMovements = False
        while self.playing:
            self.new()
            gf.checkEvents(self, settings, self.sb, self.newPlayer, self.wallGroup, USEREVENT)
            self.update()
            self.draw(settings)
            if self.playerRestarts:
                self.restartGame()

    # updates players movement; camera; and enemy movement
    def update(self):
        self.newPlayer.update(settings, self.wallGroup)
        self.camera.update(self.newPlayer)
        for x in self.wallGroup:
            if x.type == '5' or x.type == 'c':
                x.update(self.camera)

    # quits game
    def quit(self):
        pygame.quit()
        sys.exit()

    # restarts stats/restarts to first map
    def restartGame(self):
        self.makeCopies()
        self.sb.livesLeft = 3
        self.sb.coinsCollected = 0
        self.sb.score = 0
        self.seconds = 60
        self.minutes = 3
        self.mapName = self.map1
        self.previousMapName = self.map1
        self.newMap = True
        self.playerRestarts = False

    # end screen; if player finishes- either ends game or restarts
    def showEndScreen(self):
        self.mapName = self.map5
        self.new1()
        while self.stillPlaying:
            self.dt = self.clock.tick(settings.FPS) / 1000
            gf.checkEvents(self, settings, self.sb, self.newPlayer, self.wallGroup, USEREVENT)
            self.update()
            self.draw(settings)
            if self.playerRestarts == True:
                self.stillPlaying = False
            elif self.playerDone == True:
                self.stillPlaying = False


settings = Settings()
g = Game()
running = True
# main loop
while running:
    g.new()
    g.run(settings)
    g.showEndScreen()
    if g.playerDone:
        running = False
pygame.quit()
sys.exit()
