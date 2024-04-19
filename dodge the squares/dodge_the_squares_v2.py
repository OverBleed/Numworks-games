from ion import *
from kandinsky import *
from time import sleep
from random import randint

#Change the variable line 115 to change your highscore

#Screen size: 320x222p
#fill_rect(x, y, width, height, color)
#draw_string(text, x, y, [color1], [color2]) with color1 for the text et color2 for the background

class Player:
  def __init__(self, coordinates, left, right):
    self.coordinates = coordinates #coordinates [x, y]
    self.right = right #x coordinate of the right side, to detect collisions
    self.left = left #x coordinates of the left side

class Star:
  def __init__(self, coordinates, size, velocity, left, right):
    self.coordinates = coordinates #coordinates[x, y]
    self.size = size
    self.velocity = velocity #always int value
    self.right = right
    self.left = left

  def show(self):
    fill_rect(self.coordinates[0], self.coordinates[1], 10, 10, "white")

  def speed(self):
    if self.velocity < 10:
      fill_rect(self.coordinates[0], self.coordinates[1]-10, 10, 10, "black")
    elif self.velocity >= 10:
      fill_rect(self.coordinates[0], self.coordinates[1]-round(self.velocity), 10, 10, "black")
    self.coordinates[1] += round(self.velocity)
    if self.coordinates[1] >= 220:
      fill_rect(self.coordinates[0], self.coordinates[1]-round(self.velocity), 10, 10, "black")
      self.coordinates = [randint(50, 300), 0]
      self.velocity += 0.1

  def checkCollision(self):
    self.left = self.coordinates[0]
    self.right = self.coordinates[0] + self.size

    if self.coordinates[1] >= player.coordinates[1] and self.right >= player.left and self.left <= player.right:
      return True
    else: return False


fill_rect(0, 0, 320, 222, "black") #Background

stars = []
for i in range(3):
  stars.append(Star([randint(50, 300), 0], 10, randint(3, 7), 0, 10))

hour, minute = 0,0
player = Player([100, 200], 100, 145)
quit = True
averageVelocity = 0

#player movement

def playerMovement():
  player.left = player.coordinates[0]
  player.right = player.coordinates[0] + 45

  if keydown(KEY_RIGHT): #going right
    fill_rect(player.coordinates[0], player.coordinates[1], 45, 6, "white")
    fill_rect(player.coordinates[0]-45, player.coordinates[1], 45, 6, "black")
    player.coordinates [0] += 7
  
  if keydown(KEY_LEFT): #going left
    fill_rect(player.coordinates[0], player.coordinates[1], 45, 6, "white")
    fill_rect(player.coordinates[0]+45, player.coordinates[1], 45, 6, "black")
    player.coordinates[0] -= 7

def starsStuff(starObj):
  starObj.show()
  starObj.speed()

while quit:
  sleep(0.02)
  playerMovement()

  for i in range(len(stars)):
    starsStuff(stars[i])

    if stars[i].checkCollision():
      quit = False
      break
    
    averageVelocity += stars[i].velocity
    if i == len(stars) - 1:
      averageVelocity = round(averageVelocity / len(stars), 1)


  if keydown(KEY_EXE): #to pause
    while keydown(KEY_EXE): pass
    while not keydown(KEY_EXE): pass
    while keydown(KEY_EXE): pass
  

  draw_string("Score : " + str(averageVelocity), 5, 5, "white", "black") #print an average velocity of all stars
  fill_rect(player.coordinates[0], player.coordinates[1], 45, 6, "white")

highscore = averageVelocity #change this variable to your current highscore

while 1:
  fill_rect(0, 0, 320, 222, "black")
  draw_string("You lost", 120, 45, "white", "black")
  draw_string("Score : " + str(averageVelocity), 110, 65, "white", "black") #show score
  draw_string("Highscore : " + str(highscore), 90, 85, "white", "black")