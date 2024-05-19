from ion import *
from kandinsky import fill_rect, draw_string
from time import sleep

# created by overbleed on 09/11/2023

#Screen size: 320x222p
#fill_rect(x, y, width, height, color)
#draw_string(text, x, y, [color1], [color2]) with color1 for the text et color2 for the background
#screen is 13 by 8 tiles (x=13, y=8)


file = open("sprites.py", "r")
buffer = file.readlines()
bufferIndex = [[14, 16, 0, 16], [], [], []]
spriteMemory = [[], [], [], []]


#world map and tiles
tilesSpritesIndex = [[13, 15, 69, 84], [13, 15, 85, 100]]
bufferIndex[1] = tilesSpritesIndex[0]
file = open("tilemap.py", "r")
tileMapBuffer = file.readlines()
tileMapBufferIndex = [[0, 8], [9, 17], [18, 26], [27, 35]] #first one is empty for debugging
tileMap = []
collisionMap = []
gridMap = ["030",
           "210",
           "000"]

x1, y1 = 10, 10

#player variables
playerSpriteIndex = [[0, 16], [17, 33], [34, 50], [51, 67]]
x, y = 10, 10
willCollide = [0, 0, 0, 0] #[up, right, down, left] ; 0 is for no collisions and 1 is for a collision
playerPositionOnGrid = [1, 1]
playerGridMapLocation = [1, 1]
playerGridMapNumber = int(gridMap[1][1])


#moves sprites from storage to memory, can hold up to 4 at once
def spriteBuffer(buffer):
    global spriteMemory
    
    #player
    for i in range (bufferIndex[0][2], bufferIndex[0][3]):
        spriteMemory[0].append(buffer[i])

    #tiles
    for i in range(tileMapBufferIndex[playerGridMapNumber][0], tileMapBufferIndex[playerGridMapNumber][1]):
        tileMap.append(tileMapBuffer[i])

    for i in range (bufferIndex[1][2], bufferIndex[1][3]):
        spriteMemory[1].append(buffer[i])


#draws a two-colors sprite
def spriteRenderer(sprite, length, width, size, location, c1="black", c2="white"):
    for j in range (width):
        for i in range (length):
            color = sprite[j][i]
            if color == "1": fill_rect(location[0] + (i * size), location[1] + (j * size), size, size, c1)
            else: pass

def loadMap(tilemap):
    global bufferIndex

    for j in range (len(tilemap)):
        for i in range (len(tilemap[j])):
            if tilemap[j][i] == "1":
                bufferIndex[1] = tilesSpritesIndex[1]
                spriteBuffer(buffer)
                spriteRenderer(spriteMemory[1], bufferIndex[1][0], bufferIndex[1][1], 2, [x1 + (i * 26) - 26, y1 + (j * 30) - 30])
            elif tilemap[j][i] == "2":
                bufferIndex[1] = tilesSpritesIndex[0]
                spriteBuffer(buffer)
                spriteRenderer(spriteMemory[1], bufferIndex[1][0], bufferIndex[1][1], 2, [x1 + (i * 26) - 26, y1 + (j * 30) - 30])
            else: pass
            spriteMemory[1].clear()

def playerCollisions(direction):
    if direction == 0: #up
        if collisionMap[playerPositionOnGrid[0] - 1][playerPositionOnGrid[1]] == "2":
            willCollide[0] = 1
        else: willCollide[0] = 0

    if direction == 1: #right
        if collisionMap[playerPositionOnGrid[0]][playerPositionOnGrid[1] + 1] == "2":
            willCollide[1] = 1
        else: willCollide[1] = 0

    if direction == 2: #down
        if collisionMap[playerPositionOnGrid[0] + 1][playerPositionOnGrid[1]] == "2":
            willCollide[2] = 1
        else: willCollide[2] = 0

    if direction == 3: #left
        if collisionMap[playerPositionOnGrid[0]][playerPositionOnGrid[1] - 1] == "2":
            willCollide[3] = 1
        else: willCollide[3] = 0

def checkGridChange(direction):
    global x, y
    global playerGridMapLocation, playerGridMapNumber

    if direction == 0: #up
        y = 10 + 5 * 30
        playerGridMapLocation[0] -= 1
        playerPositionOnGrid[0] = 6

    elif direction == 1: #right
        x = 10
        playerGridMapLocation[1] += 1
        playerPositionOnGrid[1] = 1

    elif direction == 2: #down
        y = 10
        playerGridMapLocation[0] += 1
        playerPositionOnGrid[0] = 1

    elif direction == 3: #left
        x = 10 + 10 * 26
        playerGridMapLocation[1] -= 1
        playerPositionOnGrid[1] = 11
        
    playerGridMapNumber = int(gridMap[playerGridMapLocation[0]][playerGridMapLocation[1]])



def playerMovement():
    global x, y

    if keydown(KEY_DOWN):
        bufferIndex[0][3] = playerSpriteIndex[0][1]
        bufferIndex[0][2] = playerSpriteIndex[0][0] #changes sprite
        if  willCollide[2] == 0:
            y += 30
            playerPositionOnGrid[0] += 1
            if playerPositionOnGrid[0] >= 7:
                checkGridChange(2)
            refreshEverything()
            fill_rect(x, y, 26, 30, "white")

    if keydown(KEY_UP):
        bufferIndex[0][3] = playerSpriteIndex[1][1]
        bufferIndex[0][2] = playerSpriteIndex[1][0] 
        if willCollide[0] == 0:
            y -= 30
            playerPositionOnGrid[0] -= 1
            if playerPositionOnGrid[0] <= 0:
                checkGridChange(0)
            refreshEverything()
            fill_rect(x, y, 26, 30, "white")

    if keydown(KEY_LEFT):
        bufferIndex[0][3] = playerSpriteIndex[2][1]
        bufferIndex[0][2] = playerSpriteIndex[2][0]
        if willCollide[3] == 0:
            x -= 26
            playerPositionOnGrid[1] -= 1
            if playerPositionOnGrid[1] <= 0:
                checkGridChange(3)
            refreshEverything()
            fill_rect(x, y, 26, 30, "white")
            

    if keydown(KEY_RIGHT):
        bufferIndex[0][3] = playerSpriteIndex[3][1]
        bufferIndex[0][2] = playerSpriteIndex[3][0]
        if willCollide[1] == 0:
            x += 26
            playerPositionOnGrid[1] += 1
            if playerPositionOnGrid[1] >= 12:
                checkGridChange(1)
            refreshEverything()
            fill_rect(x, y, 26, 30, "white")


def refreshEverything():
    spriteBuffer(buffer)
    fill_rect(0, 0, 350, 250, "white")
    loadMap(tileMap)



refreshEverything()

while 1:
    spriteBuffer(buffer)

    spriteRenderer(spriteMemory[0], bufferIndex[0][0], bufferIndex[0][1], 2, [x,y]) #player

    spriteMemory[0].clear()

    collisionMap = tileMap[:]
    tileMap.clear()

    for i in range(0, 4):
        playerCollisions(i)

    if keydown(KEY_FIVE):
        playerGridMapNumber = 2

    playerMovement()