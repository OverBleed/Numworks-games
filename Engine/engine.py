from math import sqrt, pi, sin, cos
from time import sleep
from ion import *

try:
  import os
  if hasattr(os, "environ"):
    os.environ['KANDINSKY_ZOOM_RATIO'] = "4"
    os.environ['KANDINSKY_OS_MODE'] = "0"
except: pass
from kandinsky import fill_rect, set_pixel, draw_string

# screen is 320x222

engineRatio = 1.96

MIN_ENGINE_RPM = 700
MAX_ENGINE_RPM = 8500
GEAR_RATIOS = [4.5, 2.923, 1.944, 1.407, 1.129, 0.969]

def rpm(ratio):
    return (sqrt(0.20 * ratio) * 1000)

def engine(gear=0):
    global engineRatio

    #gear 0 is neutral

    # keep the lowest rpm around 1000
    if engineRatio <= 4:
        engineRatio += 1 / sqrt(0.25 * engineRatio) + 1.25
    else:
        engineRatio -= 1 / sqrt(0.25 * engineRatio) * GEAR_RATIOS[gear] + 1

    #makes the engine rev at high rpm
    if engineRatio >= 256:
        engineRatio -= 40

    if keydown(KEY_UP):
        engineRatio += 2.25 * GEAR_RATIOS[gear]

        if engineRatio >= 200:
            engineRatio += 10
    

def displayGauge(var, length, width, pos, color, max, min=0, borders=True): #pos is a list [x, y], length is x, width is y
    l = (length / max) * var

    fill_rect(pos[0], pos[1], round(l), width, color)

    if borders == True:
        fill_rect(pos[0], pos[1] + width, length, 3, "black") #bottom
        fill_rect(pos[0] + length, pos[1], 3, width, "black") #left
        fill_rect(pos[0], pos[1] - 3, length, 3, "black")
        fill_rect(pos[0] - 3, pos[1], 3, width, "black")

def draw_line(x, y, length, angle, color="black"):
    while length >= 0:
        a = round(cos(angle)*length) + x
        b = -round(sin(angle)*length) + y

        set_pixel(a, b, color)

        length -= 1

def circle(x, y, width, size=2*pi):
    teta = 7*pi/6
    teta0 = teta

    while teta > teta0 - size:
        a = round(cos(teta)*width) + x
        b = -round(sin(teta)*width) + y
        teta -= pi/60

        set_pixel(a, b, "black")

def tachometer(var, x, y, length, showNumber=False):
    teta = -sqrt(0.20*var)/2 - 5*pi/6

    # fill_rect(x-length, y-length, 2*length, 2*length, "white")
    draw_line(x, y, length-1, teta, "red")
    circle(x, y, length, 7*pi/6)
    if showNumber: draw_string(str(round(rpm(var))), int(x-(length/3)), int(y+(length/3)))
    sleep(0.005)


while 1:
    sleep(0.001)
    fill_rect(0, 0, 320, 222, "white")

    engineRPM = rpm(engineRatio)

    # displayGauge(engineRPM, 100, 10, [50, 50], "red", MAX_ENGINE_RPM, MIN_ENGINE_RPM)
    tachometer(engineRatio, 23, 200, 20, True)

    engine(5)