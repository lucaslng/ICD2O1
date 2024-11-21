import pygame, sys
from pygame.locals import *
from random import randint
import math

WIDTH = 360
HEIGHT = 300
red = (255,0,0)
orange = (255, 127, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
violet = (75, 0, 130)
purple = (148, 0, 211)
black = (0,0,0)
white = (255,255,255)
ground = (70, 109, 29)
sky = (198, 252, 255)
sun = (249, 215, 28)
wood = (133, 94, 66)
tree = (92, 169, 4)
water = (28, 163, 236)
rainbowColors = (red, orange, yellow, green, blue, violet, purple)
pi = math.pi
pygame.init()
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
arc_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption('Landscape')
clock = pygame.time.Clock()

def drawCloud(xpos, ypos, length):
  for i in range(length):
    x = xpos + (i * 26)
    pygame.draw.circle(DISPLAYSURF, white, (x, ypos), 25)
    
def drawTree(xpos, height):
  ypos = 200
  pygame.draw.rect(DISPLAYSURF, wood, (xpos, ypos-30, 8, 30))
  for i in range(height):
    shift = i * 10
    pygame.draw.polygon(DISPLAYSURF, tree, [(xpos-10, ypos-30-shift), (xpos+4, ypos-45-shift), (xpos+18, ypos-30-shift)])
   
while True:

  DISPLAYSURF.fill(sky)

#-----------------------------------

  rainbowShift = 0
  for color in rainbowColors:
    pygame.draw.arc(arc_surface, color, (140, 120+rainbowShift, 120, 50), pi, pi*2, 10)
    rainbowShift += 11
  flipped_arc_surface = pygame.transform.flip(arc_surface, False, True)
  DISPLAYSURF.blit(flipped_arc_surface, (0, 0))
  pygame.draw.rect(DISPLAYSURF, ground, (0, 200, 360, 300))
  pygame.draw.circle(DISPLAYSURF, sun, (70, 70), 40)
  drawCloud(85, 95, 3)
  drawCloud(220, 60, 4)
  pygame.draw.arc(DISPLAYSURF, water, (-200, 230, 700, 200), 0, 10, 38)
  
  
  
  for i in range(5):
    drawTree(randint(15, 340), randint(2, 5))
  
  #-----------------------------------
  
  for event in pygame.event.get():
      if event.type == QUIT:
         pygame.quit()
         sys.exit()
 
  pygame.display.update()
  clock.tick(2)
#end game loop
