import sys
import pygame
from wall import Wall
from characters import *
from player import Player


# checks all events/updates characters
def checkEvents(g, settings, sb, player, walls, USEREVENT):
    # if user hasn't reached flag (at flag- automated movement)
    if not settings.endingMovements:
        updateGoomba(walls)
        checkCollisions(g, settings, player, walls, sb)
        checkGoombaCollision(walls)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                    checkKeyDown(event, player)
            elif event.type == pygame.KEYUP:
                    checkKeyUp(event, player)
            if event.type == USEREVENT + 1 and g.mapName != g.map4 and g.mapName != g.map5:
                if g.minutes == 0 and g.seconds == 0:
                    g.previousMapName = g.mapName
                    g.mapName = g.map4
                    g.newMap = True
                elif g.seconds > 0:
                    g.seconds -= 1
                else:
                    g.minutes -=1
                    g.seconds = 60
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           sys.exit()


# checks collisions between player and wall
def checkCollisions(g, settings, player, walls, sb):
    # for checking if going right (removes coins/ removes life if player hits goomba)
    checkLeftRightMovement(g, settings, player, walls, sb)
    checkUpDownMovement(g, settings, player, walls, sb)

    # for checking if runner is pressed on the ground- if not- falls until reaches ground


# checks player and moving right/left- includes hitting coins & goombas
def checkLeftRightMovement(g, settings, player, walls, sb):
    # for checking if player can move right
    numR = 10
    for x in walls:
        if x.leftEdge <= player.rightEdge and player.rightEdge - x.leftEdge <= 5:
            if (x.topEdge < player.bottomEdge < x.bottomEdge) or (x.topEdge < player.topEdge < x.bottomEdge) or \
                    (x.topEdge == player.topEdge and player.bottomEdge == x.bottomEdge):
                # removes coins/adds to score
                if x.type == '6':
                    sb.addScore(50)
                    g.mapName.updateMap('coin', x.x, x.y)
                    walls.remove(x)
                    sb.collectCoin(1)
                # restarts level if player hits enemy
                elif x.type == '5':
                    takeOffLife(g, sb)
                # for when user jumps onto the end flag- starts end movements
                elif x.type == 'E':
                    x.changeImage()
                    if player.topEdge <= settings.tileSize * 8:
                        sb.score += 5000
                    elif player.topEdge <= settings.tileSize * 12:
                        sb.score += 3000
                    elif player.topEdge <= settings.tileSize * 16:
                        sb.score += 2000
                    else:
                        sb.score += 1000
                    settings.endingMovements = True
                # if the user is about to hit a wall walking right
                else:
                    numR = x.leftEdge - player.rightEdge
                    if numR != 0:
                        player.rightV = numR
                        player.update(settings, walls)
                        player.movingRight = False
                        player.canMoveRight = False
                    else:
                        player.rightV = numR
                        player.movingRight = False
                        player.canMoveRight = False

    # for if the player is not next to any walls on their right
    if numR == 10:
        player.canMoveRight = True
        player.rightV = settings.playerSpeed

    # for checking if going left (removes coins/ removes life if player hits goomba)
    numL = 10
    for x in walls:
        if x.rightEdge <= player.leftEdge and abs(player.leftEdge - x.rightEdge) <= 5:
            if (x.topEdge < player.bottomEdge < x.bottomEdge) or (x.topEdge < player.topEdge < x.bottomEdge) or \
                    (x.topEdge == player.topEdge and player.bottomEdge == x.bottomEdge):
                # removes coins/adds to score
                if x.type == '6':
                    sb.addScore(50)
                    g.mapName.updateMap('coin', x.x, x.y)
                    walls.remove(x)
                    sb.collectCoin(1)
                # restarts level if player hits enemy
                elif x.type == '5':
                    takeOffLife(g, sb)
                # if the user is about to hit a wall walking left
                else:
                    numL = player.leftEdge - x.rightEdge
                    if numL != 0:
                        player.leftV = numL
                        player.update(settings, walls)
                        player.movingLeft = False
                        player.canMoveLeft = False
                    else:
                        player.leftV = numL
                        player.movingLeft = False
                        player.canMoveLeft = False
    # for if the player is not next to any walls on their left
    if numL == 10:
        player.canMoveLeft = True
        player.leftV = settings.playerSpeed


# checks player and moving up/down- includes hiting coins & goombas
def checkUpDownMovement(g, settings, player, walls, sb):
    # for if user can move down
    canMoveDown1 = True
    for x in walls:
        if x.topEdge == player.bottomEdge:
            if (x.leftEdge < player.leftEdge < x.rightEdge) or (x.leftEdge < player.rightEdge < x.rightEdge) or \
                    (x.leftEdge ==player.leftEdge and x.rightEdge == player.rightEdge):
                # for if player jumps onto goomba
                if x.type == '5':
                    sb.addScore(100)
                    walls.remove(x)
                    player.jumping = True
                    player.falling = False
                # if player falls down a hole
                elif x.type == 'l':
                    takeOffLife(g, sb)
                    walls.remove(x)
                # if player is already on the groun
                else:
                    canMoveDown1 = False
                    player.canMoveDown = False
                    player.falling = False
    # if the player is on the ground already
    if canMoveDown1 and not player.jumping:
        player.falling = True
        player.canMoveDown = True

    # for checking to see that, if while jumping, player hits a ceiling/wall
    for x in walls:
        if x.bottomEdge == player.topEdge:
            if (x.leftEdge < player.leftEdge < x.rightEdge) or (x.leftEdge < player.rightEdge < x.rightEdge) or \
                    (x.leftEdge == player.leftEdge and x.rightEdge == player.rightEdge):
                # if player hits a coin
                if x.type == '6':
                    sb.addScore(50)
                    g.mapName.updateMap('coin', x.x, x.y)
                    walls.remove(x)
                    sb.collectCoin(1)
                # if player hits the ceiling- makes player start falling
                else:
                    player.jumping = False
                    player.miniJumping = False
                    player.falling = True


# checks for if player is moving/presses quit
def checkKeyDown(event, player):
    if event.key == pygame.K_RIGHT:
        player.movingRight = True
    if event.key == pygame.K_LEFT:
        player.movingLeft = True
    if event.key == pygame.K_UP:
        player.movingUp = True
    if event.key == pygame.K_DOWN:
        player.movingDown = True
        player.jumping = False
        player.miniJumping = False

    if event.key == pygame.K_ESCAPE:
        sys.exit()


# for if player stops moving
def checkKeyUp(event, player):
    if event.key == pygame.K_RIGHT:
        player.movingRight = False
    elif event.key == pygame.K_LEFT:
        player.movingLeft = False
    elif event.key == pygame.K_UP:
        player.movingUp = False
    elif event.key == pygame.K_DOWN:
        player.movingDown = False


# moves each goomba
def updateGoomba(walls):
    for x in walls:
        if x.type == '5':
            x.moveChar()


# if hit by enemy, takes off a life; shows 'gameOver' screen if out of lives
def takeOffLife(g, sb):
    if sb.livesLeft >= 0:
        g.new1()
        sb.lostALife()
    if sb.livesLeft < 0:
        g.previousMapName = g.mapName
        g.mapName = g.map4
        g.newMap = True


# checks collision between goomba and walls
def checkGoombaCollision(walls):
    for x in walls:
        if x.type == '5':
            leftEdge = x.leftEdge
            rightEdge = x.rightEdge
            topEdge = x.topEdge - 32
            bottomEdge = x.bottomEdge
            for m in walls:
                if m.leftEdge != leftEdge and m.rightEdge != rightEdge:
                    # if goomba is about to hit a wall, changes direction of the goomba
                    if abs(m.rightEdge - leftEdge) <= 2:
                        if (m.bottomEdge == bottomEdge):
                            x.switch()
                    if abs(m.leftEdge - rightEdge) <= 2:
                        if (m.bottomEdge == bottomEdge):
                            x.switch()


# goes through map/determnines which block is making what
# determines where the player spawns
def findWhichType(g,sb, tile, col, row, settings):
    # 1 = ground, 2 = border; 3 = jump boxes;
    # 5 = goomba; 6 = coins; 7 = tube; b = tile boxes
    # m = mystery boxes; n = hit mystery boxes; E = end flad
    # T = end castle; d = door to end castle
    # l = lava
    if tile == '1':
        wall = Wall(g, col, row, settings, '1')
        g.wallGroup.add(wall)
    elif tile == '2':
        wall = Wall(g, col, row, settings, '2')
        g.wallGroup.add(wall)
    elif tile == '3':
        wall = Wall(g, col, row, settings, '3')
        g.wallGroup.add(wall)
    elif tile == '5':
        character = Characters(g, col, row, settings, '5')
        g.wallGroup.add(character)
    elif tile == '6':
        character = Coins(g, col, row, settings, '6')
        g.wallGroup.add(character)
    elif tile == '7':
        wall = Wall(g, col, row, settings, '7')
        g.wallGroup.add(wall)
    elif tile == 'b':
        wall = Wall(g, col, row, settings, 'b')
        g.wallGroup.add(wall)
    elif tile == 'm':
        wall = Wall(g, col, row, settings, 'm')
        g.wallGroup.add(wall)
    elif tile == 'n':
        wall = Wall(g, col, row, settings, 'n')
        g.wallGroup.add(wall)
    elif tile == 'E':
        wall = Wall(g, col, row, settings, 'E')
        g.wallGroup.add(wall)
    elif tile == 'l':
        wall = Wall(g, col, row, settings, 'l')
        g.wallGroup.add(wall)
    elif tile == 'T':
        wall = Wall(g, col, row, settings, 'T')
        g.wallGroup.add(wall)
        wall2 = Wall(g, col + 2, row + 4, settings, 'd')
        g.wallGroup.add(wall2)

    # for determining where the player is drawn (ie- P or O)
    if tile == 'P' or tile == 'O':
        # for first spawning
        if g.previousMapName == g.map1 and g.mapName == g.map1:
            if tile == "P":
                g.newPlayer = Player(g, sb, col, row, settings, g.screen, settings)
        # for from underground to map1
        elif g.previousMapName == g.map2 and g.mapName == g.map1:
            if tile == "O":
                g.newPlayer = Player(g, sb, col, row, settings, g.screen, settings)
        # for from map1 to underground
        elif g.previousMapName == g.map1 and g.mapName == g.map2:
            if tile == "P":
                g.newPlayer = Player(g, sb, col, row, settings, g.screen, settings)
        # for from underground to map2
        elif g.previousMapName == g.map2 and g.mapName == g.map3:
            if tile == "P":
                g.newPlayer = Player(g, sb, col, row, settings, g.screen, settings)
        # for from map2 to underground
        elif g.previousMapName == g.map3 and g.mapName == g.map2:
            if tile == "O":
                g.newPlayer = Player(g, sb, col, row, settings, g.screen, settings)
        elif g.mapName == g.map4:
            if tile == "P":
                g.newPlayer = Player(g, sb, col, row, settings, g.screen, settings)
        elif g.mapName == g.map5:
            if tile == "P":
                g.newPlayer = Player(g, sb, col, row, settings, g.screen, settings)


# determines which map it should change to
def findWhichMap(g, x, sb):
    # for going from map1 to undergroundMap
    if x.type == '7' and x.topEdge == g.newPlayer.bottomEdge and g.newPlayer.movingDown and g.mapName == g.map1:
        if x.leftEdge <= g.newPlayer.leftEdge <= x.rightEdge:
            g.previousMapName = g.map1
            g.mapName = g.map2
            g.newMap = True
    # for going from undergroundMap to map
    elif x.type == '7' and x.topEdge == g.newPlayer.bottomEdge and g.newPlayer.movingDown and \
            g.mapName == g.map2 and x.leftEdge < 800:
        if x.leftEdge <= g.newPlayer.leftEdge <= x.rightEdge:
            g.previousMapName = g.map2
            g.mapName = g.map1
            g.newMap = True
    # for going from undergroundMap to map2
    elif x.type == '7' and x.topEdge == g.newPlayer.bottomEdge and g.newPlayer.movingDown and \
            g.mapName == g.map2 and x.leftEdge > 800:
        if x.leftEdge <= g.newPlayer.leftEdge <= x.rightEdge:
            g.previousMapName = g.map2
            g.mapName = g.map3
            g.newMap = True
   # for going from map2 to undergroundMap
    elif x.type == '7' and x.topEdge == g.newPlayer.bottomEdge and g.newPlayer.movingDown and g.mapName == g.map3:
            if x.leftEdge <= g.newPlayer.leftEdge <= x.rightEdge:
                g.previousMapName = g.map3
                g.mapName = g.map2
                g.newMap = True
                
