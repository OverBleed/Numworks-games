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

fill_rect(0, 0, 320, 222, "black") #Background

star1 = Star([randint(50, 300), 0], 10, randint(3, 7), 0, 10)
star2 = Star([randint(50, 300), 0], 10, randint(3, 7), 0, 10)
star3 = Star([randint(50, 300), 0], 10, randint(3, 7), 0, 10)
hour, minute = 0,0
player = Player([100, 200], 100, 145)

#stars

def s1():
  fill_rect(star1.coordinates[0], star1.coordinates[1], 10, 10, "white")
  star1.left = star1.coordinates[0]
  star1.right = star1.coordinates[0] + star1.size
  
  if star1.velocity < 10:
    fill_rect(star1.coordinates[0], star1.coordinates[1]-10, 10, 10, "black")
  elif star1.velocity >= 10:
    fill_rect(star1.coordinates[0], star1.coordinates[1]-round(star1.velocity), 10, 10, "black")
  star1.coordinates[1] += round(star1.velocity)
  if star1.coordinates[1] >= 220:
    fill_rect(star1.coordinates[0], star1.coordinates[1]-round(star1.velocity), 10, 10, "black")
    star1.coordinates = [randint(50, 300), 0]
    star1.velocity += 0.1

def s2():
  fill_rect(star2.coordinates[0], star2.coordinates[1], 10, 10, "white")
  star2.left = star2.coordinates[0]
  star2.right = star2.coordinates[0] + star2.size

  if star2.velocity < 10:
    fill_rect(star2.coordinates[0], star2.coordinates[1]-10, 10, 10, "black")
  elif star2.velocity >= 10:
    fill_rect(star2.coordinates[0], star2.coordinates[1]-round(star2.velocity), 10, 10, "black")

  star2.coordinates[1] += round(star2.velocity)
  if star2.coordinates[1] >= 220:
    fill_rect(star2.coordinates[0], star2.coordinates[1]-round(star2.velocity), 10, 10, "black")
    star2.coordinates = [randint(50, 300), 0]
    star2.velocity += 0.1

def s3():
  fill_rect(star3.coordinates[0], star3.coordinates[1], 10, 10, "white")
  star3.left = star3.coordinates[0]
  star3.right = star3.coordinates[0] + star3.size

  if star3.velocity < 10:
    fill_rect(star3.coordinates[0], star3.coordinates[1]-10, 10, 10, "black")
  elif star3.velocity >= 10:
    fill_rect(star3.coordinates[0], star3.coordinates[1]-round(star3.velocity), 10, 10, "black")
  
  star3.coordinates[1] += round(star3.velocity)
  if star3.coordinates[1] >= 220:
    fill_rect(star3.coordinates[0], star3.coordinates[1]-round(star3.velocity), 10, 10, "black")
    star3.coordinates = [randint(50, 300), 0]
    star3.velocity += 0.1

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

while True:
  sleep(0.02)
  s1()
  s2()
  s3()
  if star1.coordinates[1] >= player.coordinates[1] and star1.right >= player.left and star1.left <= player.right:
    break
  if star2.coordinates[1] >= player.coordinates[1] and star2.right >= player.left and star2.left <= player.right:
    break
  if star3.coordinates[1] >= player.coordinates[1] and star3.right >= player.left and star3.left <= player.right:
    break

  if keydown(KEY_EXE): #to pause
    while keydown(KEY_EXE): pass
    while not keydown(KEY_EXE): pass
    while keydown(KEY_EXE): pass
  
  draw_string("Score : " + str(round((star1.velocity + star2.velocity + star3.velocity)/3, 1)), 5, 5, "white", "black") #print an average velocity of all stars
  fill_rect(player.coordinates[0], player.coordinates[1], 45, 6, "white")
  playerMovement()

highscore = round((star1.velocity + star2.velocity + star3.velocity)/3, 1) #change this variable to your current highscore

fill_rect(0, 0, 320, 222, "black")
draw_string("You lost", 120, 45, "white", "black")
draw_string("Score : " + str(round((star1.velocity + star2.velocity + star3.velocity)/3, 1)), 110, 65, "white", "black") #show score
draw_string("Highscore : " + str(highscore), 90, 85, "white", "black")
