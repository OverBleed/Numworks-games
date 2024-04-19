from ion import *
from kandinsky import *
from time import sleep
from random import randint

# created by overbleed on 18/04/2023
# credits to the dudes who ported the kandinsky and ion modules to pc
# version 1.0.1

#Screen size: 320x222p
#fill_rect(x, y, width, height, color)
#draw_string(text, x, y, [color1], [color2]) with color1 for the text et color2 for the background

alive = 1
score = 0

#playerVariables
pCoordinates = [40, 100]
pSize = 15
pTop = pCoordinates[1]
pBottom = pCoordinates[1] + pSize
pLeft = pCoordinates[0]
pRight = pCoordinates[0] + pSize
pDirection = "u" #u, d, r, l for respectively up, down, right, left

#bullet
bCoordinates = []
bDirection = []
bIndex = 0 #it means that there isn't any bullets
bSize = 10

#enemy
eCoordinates = [[100, 100]]
eSize = 15
eTop = [eCoordinates[0][1]]
eBottom = [eCoordinates[0][1] + eSize]
eLeft = [eCoordinates[0][0]]
eRight = [eCoordinates[0][0] + eSize]
eQuantity = 8
eInvicibiltyFrames = [0]
eSpawnAreas = [[[0, 320], [0, 0]], [[320, 320], [0, 220]], [[0, 320], [220, 220]], [[0, 0], [0, 220]]] # top, right, bottom, left

for i in range (8):
    eInvicibiltyFrames.append(0)
    eCoordinates.append([150, 100])
    eTop.append(eCoordinates[0][1])
    eBottom.append(eCoordinates[0][1] + eSize)
    eLeft.append(eCoordinates[0][0])
    eRight.append(eCoordinates[0][0] + eSize)

def collisions():
    global pTop
    global pBottom
    global pLeft
    global pRight

    global eTop
    global eBottom
    global eLeft
    global eRight

    global alive
    global score

    #refreshing the hitboxes
    pTop = pCoordinates[1]
    pBottom = pCoordinates[1] + pSize
    pLeft = pCoordinates[0]
    pRight = pCoordinates[0] + pSize

    for i in range (eQuantity):
        eTop[i] = eCoordinates[i][1]
        eBottom[i] = eCoordinates[i][1] + eSize
        eLeft[i] = eCoordinates[i][0]
        eRight[i] = eCoordinates[i][0] + eSize


    for i in range (eQuantity):
        eInvicibiltyFrames[i] -= 1

        #between player and enemies
        if pLeft <= eRight[i] and pRight >= eLeft[i] and pBottom >= eTop[i] and pTop <= eBottom[i]:
            alive = 0
        #between bullets and enemies
        for a in range (bIndex):
            if eRight[i] >= bCoordinates[a][0] and eLeft[i] <= bCoordinates[a][0] and eBottom[i] >= bCoordinates[a][1] and eTop[i] <= bCoordinates[a][1]:
                if eInvicibiltyFrames[i] <= 0: #so you can't spawn kill
                    score += 1
                    eCoordinates[i][0] = 100 #replace the enemy in the middle of the screen
                    eCoordinates[i][1] = 100
                    eInvicibiltyFrames[i] = 25
                    enemySpawn(i)

def enemySpawn(index):
    area = randint(0, 3)
    randomSpawnX = randint(eSpawnAreas[area][0][0], eSpawnAreas[area][0][1])
    randomSpawnY = randint(eSpawnAreas[area][1][0], eSpawnAreas[area][1][1])

    eCoordinates[index][0] = randomSpawnX
    eCoordinates[index][1] = randomSpawnY

def enemyMovement():
    for i in range(eQuantity):
        if eLeft[i] <= pLeft:
            eCoordinates[i][0] += 1
        else:
            eCoordinates[i][0] -= 1
        if eTop[i] <= pTop:
            eCoordinates[i][1] += 1
        else:
            eCoordinates[i][1] -= 1

def playerMovement():
    global pDirection
    if keydown(KEY_RIGHT):
        pCoordinates[0] += 5
        pDirection = "r"
    if keydown(KEY_LEFT):
        pCoordinates[0] -= 5
        pDirection = "l"
    if keydown(KEY_UP):
        pCoordinates[1] -= 5
        pDirection = "u"
    if keydown(KEY_DOWN):
        pCoordinates[1] += 5
        pDirection = "d"

def bulletMovement(index):
    global bIndex

    try:
        #check the direction to see if in wich direction it has to go
        if bDirection[index] == "r": #right
            bCoordinates[index][0] += 12
        elif bDirection[index] == "l": #left
            bCoordinates[index][0] -= 12
        elif bDirection[index] == "d": #down
            bCoordinates[index][1] += 12
        elif bDirection[index] == "u": #up
            bCoordinates[index][1] -= 12
        
        #show the bullet
        fill_rect(bCoordinates[index][0], bCoordinates[index][1], bSize, bSize, "yellow")

        #collider with screen limit
        if bCoordinates[index][0] >= 340 or bCoordinates[index][0] <= 0 or bCoordinates[index][1] >= 240 or bCoordinates[index][1] <= 0:
            bCoordinates.pop(index)
            bDirection.pop(index)
            bIndex -= 1
    except:
        pass


while alive:
    sleep(0.02)

    #basic textures
    fill_rect(0, 0, 350, 350, "white") #background
    fill_rect(pCoordinates[0], pCoordinates[1], pSize, pSize, "black") #player
    

    draw_string(str(score), 0, 0, "black", "white")

    for i in range (eQuantity):
        fill_rect(eCoordinates[i][0], eCoordinates[i][1], eSize, eSize, "green") #enemy

    #shoot bullets
    if keydown(KEY_OK):
        if bIndex <= 10: #limits the number of bullets on the screen
            bDirection.append(pDirection)
            bIndex += 1
            bCoordinates.append([pCoordinates[0] + 3, pCoordinates[1] + 3]) # +3 is for the bullet to appear in the middle of the player
    for i in range(bIndex):
        bulletMovement(i)

    enemyMovement()
    playerMovement()
    collisions()

while 1:
    fill_rect(0, 0, 350, 350, "red")