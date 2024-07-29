from ion import *
from kandinsky import fill_rect
from time import sleep

# created by overbleed on 09/11/2023

#Screen size: 320x222p
#fill_rect(x, y, width, height, color)
#draw_string(text, x, y, [color1], [color2]) with color1 for the text et color2 for the background
#screen is 13 by 8 tiles (x=13, y=8)

sprites = {
    "wall": "000011111000000110000011000100000000010110000000001111000000000111011000001101100111111100110001000100011000100010001100010001000110001000100011000100010001010010001001000111000111000000111110000",
    "grass": "000000000011001111000110010100010100010001000110011000110001011000100100001110100001000000111000000100100011000001100110001010010010011100101001111100010010000010001000100001101011110000011000110",
    "player_left": "00001111110000000100000010000010000000010001100000000100100000000011100111111111111000101001111110001010010011000010000000100000010000110100000011111001000000011001010000000110010100000010011110000000100001000000000111100000",
    "player_right": "00001111110000000100000010000010000000010000100000000110011100000000010111111111111001111110010100001100100101000001000000010000101100001000001001111100000010100110000000101001100000000111100100000000100001000000000111100000",
    "player_up": "00001111110000000100000010000010000000010000100000000100011000000001100111000000111010111111111101100111111110010110011110011001111000011110101101111011011011001100110101111000011110001011111101000010001100010000011100111000",
    "player_down": "00001111110000000100000010000010000000010000100000000100011100000011100110111111011010100000000101100001001000010110010010011001110000001110100111111110011001111111100101110011001110001011001101000010001100010000011100111000"
}

tileMap = {
    "default": "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
    "M_01": "22112222222222001020000012001000000200200111010222022000001002002211010111101222201011000022222222222222",
    "M_02": "22222222222222001020012012201220021100020111010111002010001002202211212112221222221211111122222222222222",
    "M_03": "22222222222222000000000002200110200111220010020010022000022200002200000000000220000000000022201222222222"
}

MAP_HEIGHT = 13
MAP_LENGTH = 8

TILE_WIDTH = 15
TILE_LENGTH = 13

#world map and tiles
tilesSpritesIndex = [[13, 15, 69, 84], [13, 15, 85, 100]]
gridMap = ["030",
           "210",
           "000"]

x1, y1 = 10, 10

#player variables and constants
playerSpriteIndex = [[0, 16], [17, 33], [34, 50], [51, 67]]
x, y = 10, 10
willCollide = [0, 0, 0, 0] #[up, right, down, left] ; 0 is for no collisions and 1 is for a collision
playerPositionOnGrid = [1, 1]
playerGridMapLocation = [1, 1]
playerCurrentSprite = "player_right"
playerCurrentMap = "M_01"

PLAYER_WIDTH = 16
PLAYER_LENGTH = 14

#draws a two-colors sprite
def spriteRenderer(sprite, length, width, size, location, c1=(0, 0, 0), c2="white"):
    for j in range (width):
        for i in range (length):
            color = sprite[i + (length*j)]
            if color == "1": 
                fill_rect(location[0] + (i * size), location[1] + (j * size), size, size, c1)

            elif color == "0" and c2 != "white":
                fill_rect(location[0] + (i * size), location[1] + (j * size), size, size, c2)

def loadMap(tilemap):
    for j in range (MAP_LENGTH):
        for i in range (MAP_HEIGHT):
            if tilemap[i + (TILE_LENGTH*j)] == "1":
                spriteRenderer(sprites["grass"], TILE_LENGTH, TILE_WIDTH, 2, [x1 + (i * 26) - 26, y1 + (j * 30) - 30])

            elif tilemap[i + (TILE_LENGTH*j)] == "2":
                spriteRenderer(sprites["wall"], TILE_LENGTH, TILE_WIDTH, 2, [x1 + (i * 26) - 26, y1 + (j * 30) - 30])

            else: pass


def playerMovement():
    global x, y
    global playerCurrentSprite, playerCurrentMap

    playerCollisions(tileMap[playerCurrentMap])

    if keydown(KEY_DOWN):
        if willCollide[2] == 0:
            y += 30
            refreshPlayerMovement(tileMap[playerCurrentMap])
            playerPositionOnGrid[1] += 1
            playerCurrentSprite = "player_down"
            spriteRenderer(sprites[playerCurrentSprite], PLAYER_LENGTH, PLAYER_WIDTH, 2, [x, y])

            if playerPositionOnGrid[1] >= 7:
                checkGridChange(2)
                refreshEverything()

    if keydown(KEY_UP):
        if willCollide[0] == 0:
            y -= 30
            refreshPlayerMovement(tileMap[playerCurrentMap])
            playerPositionOnGrid[1] -= 1
            playerCurrentSprite = "player_up"
            spriteRenderer(sprites[playerCurrentSprite], PLAYER_LENGTH, PLAYER_WIDTH, 2, [x, y])

            if playerPositionOnGrid[1] <= 0:
                checkGridChange(0)
                refreshEverything()

    if keydown(KEY_LEFT):
        if willCollide[3] == 0:
            x -= 26
            refreshPlayerMovement(tileMap[playerCurrentMap])
            playerPositionOnGrid[0] -= 1
            playerCurrentSprite = "player_left"
            spriteRenderer(sprites[playerCurrentSprite], PLAYER_LENGTH, PLAYER_WIDTH, 2, [x, y])

            if playerPositionOnGrid[0] <= 0:
                checkGridChange(3)
                refreshEverything()


    if keydown(KEY_RIGHT):
        if willCollide[1] == 0:
            x += 26
            refreshPlayerMovement(tileMap[playerCurrentMap])
            playerPositionOnGrid[0] += 1
            playerCurrentSprite = "player_right"
            spriteRenderer(sprites[playerCurrentSprite], PLAYER_LENGTH, PLAYER_WIDTH, 2, [x, y])

            if playerPositionOnGrid[0] >= 12:
                checkGridChange(1)
                refreshEverything()


def playerCollisions(tilemap):
    for direction in range(0, 4):
        if direction == 0: #up
            if tilemap[playerPositionOnGrid[0] + (TILE_LENGTH*(playerPositionOnGrid[1] - 1))] == "2":
                willCollide[0] = 1
            else: willCollide[0] = 0

        if direction == 1: #right
            if tilemap[playerPositionOnGrid[0] + 1 + (TILE_LENGTH*playerPositionOnGrid[1])] == "2":
                willCollide[1] = 1
            else: willCollide[1] = 0

        if direction == 2: #down
            if tilemap[playerPositionOnGrid[0] + (TILE_LENGTH*(playerPositionOnGrid[1] + 1))] == "2":
                willCollide[2] = 1
            else: willCollide[2] = 0

        if direction == 3: #left
            if tilemap[playerPositionOnGrid[0] - 1 + (TILE_LENGTH*playerPositionOnGrid[1])] == "2":
                willCollide[3] = 1
            else: willCollide[3] = 0

def checkGridChange(direction):
    global x, y
    global playerGridMapLocation, playerCurrentMap

    if direction == 0: #up
        y = 10 + 5 * 30
        playerGridMapLocation[0] -= 1
        playerPositionOnGrid[1] = 6

    elif direction == 1: #right
        x = 10
        playerGridMapLocation[1] += 1
        playerPositionOnGrid[0] = 1

    elif direction == 2: #down
        y = 10
        playerGridMapLocation[0] += 1
        playerPositionOnGrid[1] = 1

    elif direction == 3: #left
        x = 10 + 10 * 26
        playerGridMapLocation[1] -= 1
        playerPositionOnGrid[0] = 11
        
    playerGridMapNumber = int(gridMap[playerGridMapLocation[0]][playerGridMapLocation[1]])

    if playerGridMapNumber == 0: playerCurrentMap = "default"
    elif playerGridMapNumber == 1: playerCurrentMap = "M_01"
    elif playerGridMapNumber == 2: playerCurrentMap = "M_02"
    elif playerGridMapNumber == 3: playerCurrentMap = "M_03"

def refreshEverything():
    fill_rect(0, 0, 350, 230, (255, 255, 255))

    loadMap(tileMap[playerCurrentMap])
    spriteRenderer(sprites[playerCurrentSprite], PLAYER_LENGTH, PLAYER_WIDTH, 2, [x, y])

def refreshSingleTile(posx, posy, tilemap):
    if tilemap[posx + (TILE_LENGTH*posy)] == "1":
        spriteRenderer(sprites["grass"], TILE_LENGTH, TILE_WIDTH, 2, [x1 + (posx * 26) - 26, y1 + (posy * 30) - 30], (0, 0, 0), (255, 255, 255))

    elif tilemap[posx + (TILE_LENGTH*posy)] == "2":
        spriteRenderer(sprites["wall"], TILE_LENGTH, TILE_WIDTH, 2, [x1 + (posx * 26) - 26, y1 + (posy * 30) - 30], (0, 0, 0), (255, 255, 255))

    else:
        fill_rect(x1 + (posx * 26) - 26, y1 + (posy * 30) - 30, TILE_LENGTH*2, TILE_WIDTH*2, "white")

def refreshPlayerMovement(tilemap): # only refreshes the tile the player was at instead of the whole screen
    refreshSingleTile(playerPositionOnGrid[0], playerPositionOnGrid[1], tilemap)
    refreshSingleTile(playerPositionOnGrid[0] + 1, playerPositionOnGrid[1], tilemap)
    refreshSingleTile(playerPositionOnGrid[0], playerPositionOnGrid[1] + 1, tilemap)

refreshEverything()

while 1:
    playerMovement()
    # sleep(0.01)
