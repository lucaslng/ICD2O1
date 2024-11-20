import pygame, sys
from pygame.locals import *

WIDTH = 360
HEIGHT = 300
red = (255,0,0)
black = (0,0,0)
white = (255,255,255)
ground = (70, 109, 29)
sky = (198, 252, 255)
sun = (249, 215, 28)
pygame.init()
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Landscape')
   
while True:

  DISPLAYSURF.fill(sky)

#-----------------------------------
  pygame.draw.rect(DISPLAYSURF, ground, (0, 200, 360, 300))
  pygame.draw.circle(DISPLAYSURF, sun, (70, 70), 40)
  # pygame.draw.circle(DISPLAYSURF,black,(100,100),50)
  # pygame.draw.rect(DISPLAYSURF,black,(200,200,50,75))
  # pygame.draw.line(DISPLAYSURF,white,(200,50),(250,50),1)
  # pygame.draw.line(DISPLAYSURF,white,(200,60),(250,60),2)
  # pygame.draw.line(DISPLAYSURF,white,(200,70),(250,70),3)
  # pygame.draw.line(DISPLAYSURF,white,(200,80),(250,80),5)
  # pygame.draw.line(DISPLAYSURF,white,(200,90),(250,90),10)
  #-----------------------------------
  
  for event in pygame.event.get():
      if event.type == QUIT:
         pygame.quit()
         sys.exit()
 
  pygame.display.update()
#end game loop
