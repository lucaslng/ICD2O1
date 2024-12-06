from enum import Enum
import sys
import pygame as pg
from pygame.locals import *
from random import randint
import math

# constants
WIDTH = 500
HEIGHT = 500
FPS = 60
TITLE_WIDTH = 332
TITLE_HEIGHT = 102
PLAY_BUTTON_WIDTH = 320
PLAY_BUTTON_HEIGHT = 102
PLAY_BUTTON_BORDER_WIDTH = 10
HELP_BUTTON_WIDTH = PLAY_BUTTON_WIDTH
HELP_BUTTON_HEIGHT = 80
HELP_BUTTON_BORDER_WIDTH = 10
BALL_SIZE = 20
BALL_SPEED = 300/FPS
BALL_MAX_BOUNCE_ANGLE = math.radians(20)
PADDLE_SIZE = 70
PADDLE_THICKNESS = 10
PADDLE_PADDING = 10
PADDLE_SPEED = 8
PADDLE_PADDING_SIDE = 14
SCORE_FONT_SIZE = 50
WINNER_FONT_SIZE = 40
GAME_OVER_FONT_SIZE = 70
GAME_OVER_BUTTON_WIDTH = 280
GAME_OVER_BUTTON_HEIGHT = 90
GAME_OVER_BUTTON_BORDER_WIDTH = 10
WIN_SCORE = 2
FONT_FILE = "ARCADE_N.TTF"

# colors
class Colors(Enum):
  WHITE=(255,255,255)
  BLACK=(0,0,0)
  DARKGRAY=(34,31,36)
  GRAY=(106,99,103)
  RED=(245,110,100)
  BLUE=(6,186,221)

# game states
class GameState(Enum):
  MENU=0
  GAME=1
  HELP=2
gameState = GameState.MENU

# pygame init
pg.init()
SURF = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Pong with a Twist!')
clock = pg.time.Clock()


# draw button with text
class Button:
  def __init__(this,x:float,y:float,width:float,height:float,text:str,borderWidth:int,state:GameState,isImage:bool=False,fontSize=-1):
    this.text = text
    this.state = state
    this.rect = pg.Rect(x-width//2,y,width,height) # x value is the center of the button
    this.borderWidth = borderWidth
    this.innerRect = pg.Rect(this.rect.x+borderWidth,this.rect.y+borderWidth,width-2*borderWidth,height-2*borderWidth)
    this.fontSize = this.innerRect.height-borderWidth
    if fontSize!=-1: this.fontSize = fontSize
    if isImage:
      this.blit = pg.transform.scale(pg.image.load(text),this.innerRect.size)
      this.blitRect = this.innerRect
    else:
      this.font = pg.font.Font(FONT_FILE,this.fontSize)
      this.blit = this.font.render(text,True,Colors.WHITE)
      this.blitRect = pg.Rect((this.innerRect.width-this.blit.get_width())//2+this.innerRect.x,((this.innerRect.height-this.blit.get_height())//2)+this.innerRect.y,*this.blit.get_size())
  
  def isHovered(this):
    return this.rect.collidepoint(pg.mouse.get_pos())
  
  def draw(this):
    if this.isHovered():
      pg.draw.rect(SURF,Colors.WHITE,this.rect)
    else:
      pg.draw.rect(SURF,Colors.GRAY,this.rect)
    pg.draw.rect(SURF,Colors.BLACK,this.innerRect)
    SURF.blit(this.blit,this.blitRect.topleft)
  
  def pressed(this):
    global gameState
    gameState = GameState(this.state)
  
# title loop
def title():
  global gameState
  
  def initTitle():
    global titleImage,titleRect
    titleRect = pg.Rect(WIDTH//2-TITLE_WIDTH//2,HEIGHT//5,TITLE_WIDTH,TITLE_HEIGHT)
    titleImage = pg.transform.scale(pg.image.load("title.png"),(TITLE_WIDTH,TITLE_HEIGHT))
  
  def drawTitle():
    SURF.blit(titleImage,titleRect)
  
  def initButtons():
    global buttons,playButton,helpButton
    playButton = Button(WIDTH//2,HEIGHT//2,PLAY_BUTTON_WIDTH,PLAY_BUTTON_HEIGHT,"play.png",PLAY_BUTTON_BORDER_WIDTH,GameState.GAME,True)
    helpButton = Button(WIDTH//2,HEIGHT*0.7,HELP_BUTTON_WIDTH,HELP_BUTTON_HEIGHT,"How to play",HELP_BUTTON_BORDER_WIDTH,GameState.HELP,fontSize=26 )
    buttons = (playButton,helpButton)
  
  initTitle()
  initButtons()
  
  while True:
    SURF.fill(Colors.BLACK)
    
    drawTitle()
    playButton.draw()
    helpButton.draw()
    
    for event in pg.event.get():
        if event.type == QUIT:
          pg.quit()
          sys.exit()
        if pg.mouse.get_pressed()[0] and playButton.isHovered():
          for button in buttons:
            if button.isHovered():
              button.pressed()
              return
          return
    
    pg.display.flip()
    clock.tick(FPS)

# game loop
def game():
  global gameState
  
  # scores
  def resetScore():
    global redScore,blueScore
    redScore = 0
    blueScore = 0
  
  # paddle locations
  class PaddleLocation(Enum):
    LEFT=0
    RIGHT=1
    UP=2
    DOWN=3
    
  # ball
  class Ball(pg.sprite.Sprite):
    def __init__(this):
      super().__init__()
      this.image = pg.transform.scale(pg.image.load("ball.png"),(BALL_SIZE,BALL_SIZE))
      this.angle = math.radians(randint(0,360))
      this.rect = this.image.get_rect()
      this.rect.x = randint(WIDTH//2-50,WIDTH//2+50-BALL_SIZE)
      this.rect.y = randint(HEIGHT//2-50,HEIGHT//2+50-BALL_SIZE)
      this.mask = pg.mask.from_surface(this.image)
      
    def move(this):
      this.rect.x += BALL_SPEED * math.cos(this.angle)
      this.rect.y += BALL_SPEED * math.sin(this.angle)

    def isOut(this):
      global redScore,blueScore
      if this.rect.x<=0:
        blueScore += 1
        return True
      elif this.rect.y<=0:
        redScore += 1
        return True
      elif this.rect.x+BALL_SIZE>=WIDTH:
        redScore += 1
        return True
      elif this.rect.y+BALL_SIZE>=HEIGHT:
        blueScore += 1
        return True
      return False
    
    def respawn(this):
      this.rect.x = randint(WIDTH//2-50,WIDTH//2+50-BALL_SIZE)
      this.rect.y = randint(HEIGHT//2-50,HEIGHT//2+50-BALL_SIZE)
      this.angle = math.radians(randint(0,360))
    
    def draw(this):
      SURF.blit(this.image,this.rect)
    
    def bounce(this,paddleLocation:PaddleLocation,paddlePosition):
      dx = math.cos(this.angle)
      dy = math.sin(this.angle)
      if paddleLocation == PaddleLocation.LEFT or paddleLocation == PaddleLocation.RIGHT:
        ballLocation = ball.rect.y
        dx = -dx
      else:
        ballLocation = ball.rect.x
        dy = -dy
      # gets reflection, then makes the paddle go slightly in the a direction depending on where the ball hits the paddle
      this.angle = math.atan2(dy,dx) #+ (1 - 2 * (ballLocation - paddlePosition) / PADDLE_SIZE) * BALL_MAX_BOUNCE_ANGLE 

  # paddle
  class Paddle(pg.sprite.Sprite):
    global SURF,HEIGHT,PADDLE_SIZE,PADDLE_THICKNESS,PADDLE_PADDING,red,blue
    
    def __init__(this,location:PaddleLocation):
      super().__init__()
      this.previousCollisionTime = 0
      this.location = location
      if location == PaddleLocation.LEFT:
        this.position = HEIGHT//2-PADDLE_SIZE//2
        this.color = red
        this.rect = pg.Rect(PADDLE_PADDING,this.position,PADDLE_THICKNESS,PADDLE_SIZE)
        this
        this.mask = pg.mask.Mask((PADDLE_THICKNESS,PADDLE_SIZE),True)
      elif location == PaddleLocation.RIGHT:
        this.position = HEIGHT//2-PADDLE_SIZE//2
        this.color = blue
        this.rect = pg.Rect(WIDTH-PADDLE_PADDING-PADDLE_THICKNESS,this.position,PADDLE_THICKNESS,PADDLE_SIZE)
        this.mask = pg.mask.Mask((PADDLE_THICKNESS,PADDLE_SIZE),True)
      elif location == PaddleLocation.UP:
        this.position = WIDTH//2-PADDLE_SIZE//2
        this.color = blue
        this.rect = pg.Rect(this.position,PADDLE_PADDING,PADDLE_SIZE,PADDLE_THICKNESS)
        this.mask = pg.mask.Mask((PADDLE_SIZE,PADDLE_THICKNESS),True)
      elif location == PaddleLocation.DOWN:
        this.position = WIDTH//2-PADDLE_SIZE//2
        this.color = red
        this.rect = pg.Rect(this.position,HEIGHT-PADDLE_PADDING-PADDLE_THICKNESS,PADDLE_SIZE,PADDLE_THICKNESS)
        this.mask = pg.mask.Mask((PADDLE_SIZE,PADDLE_THICKNESS),True)
    
    def update(this):
      super().update()
      if this.location == PaddleLocation.LEFT: this.rect = pg.Rect(PADDLE_PADDING,this.position,PADDLE_THICKNESS,PADDLE_SIZE)
      elif this.location == PaddleLocation.RIGHT: this.rect = pg.Rect(WIDTH-PADDLE_PADDING-PADDLE_THICKNESS,this.position,PADDLE_THICKNESS,PADDLE_SIZE)
      elif this.location == PaddleLocation.UP: this.rect = pg.Rect(this.position,PADDLE_PADDING,PADDLE_SIZE,PADDLE_THICKNESS)
      elif this.location == PaddleLocation.DOWN: this.rect = pg.Rect(this.position,HEIGHT-PADDLE_PADDING-PADDLE_THICKNESS,PADDLE_SIZE,PADDLE_THICKNESS)
    
    def draw(this):
      pg.draw.rect(SURF,this.color,this.rect)
    
    def move(this,direction:bool):
      if direction:
        this.position -= min(PADDLE_SPEED,this.position-PADDLE_PADDING_SIDE)
      else:
        if this.location == PaddleLocation.LEFT or this.location == PaddleLocation.RIGHT:
          this.position += min(PADDLE_SPEED,HEIGHT-this.position-PADDLE_SIZE-PADDLE_PADDING_SIDE)
        else:
          this.position += min(PADDLE_SPEED,WIDTH-this.position-PADDLE_SIZE-PADDLE_PADDING_SIDE)
      this.update()
  
  # draw scores
  def drawScores():
    SURF.blit(font.render(str(redScore),True,Colors.WHITE),(WIDTH*0.1,HEIGHT//2-SCORE_FONT_SIZE//2))
    SURF.blit(font.render(str(blueScore),True,Colors.WHITE),(WIDTH*0.8,HEIGHT//2-SCORE_FONT_SIZE//2))

# draw game over screen
  def drawGameOver():
    SURF.blit(gameOverText,(WIDTH//2-gameOverText.get_width()//2,HEIGHT*0.15))
    SURF.blit(winnerText,(WIDTH//2-winnerText.get_width()//2,HEIGHT*0.35))
    gameOverMenuButton.draw()
  
  # element functions
  def drawPaddles():
    global paddles
    for paddle in paddles:
      paddle.draw()

  def initElements():
    global paddleLeft,paddleRight,paddleUp,paddleDown,paddles,ball,font,winnerFont,gameOverText,gameOverMenuButton
    paddleLeft = Paddle(PaddleLocation.LEFT)
    paddleRight = Paddle(PaddleLocation.RIGHT)
    paddleUp = Paddle(PaddleLocation.UP)
    paddleDown = Paddle(PaddleLocation.DOWN)
    ball = Ball()
    paddles=[paddleLeft,paddleRight,paddleUp,paddleDown]
    font = pg.font.Font("ARCADE_N.TTF",SCORE_FONT_SIZE)
    winnerFont = pg.font.Font("ARCADE_N.TTF",WINNER_FONT_SIZE)
    gameOverText = font.render("Game Over",True,Colors.WHITE)
    gameOverMenuButton = Button(WIDTH//2,HEIGHT//2,GAME_OVER_BUTTON_WIDTH,GAME_OVER_BUTTON_HEIGHT,"MENU",GAME_OVER_BUTTON_BORDER_WIDTH,GameState.MENU)

  def detectCollision():
    global previousCollisionTime
    for paddle in paddles:
      offset = paddle.rect.x - ball.rect.x, paddle.rect.y - ball.rect.y
      if ball.mask.overlap(paddle.mask,offset) and pg.time.get_ticks() - paddle.previousCollisionTime > 180:
        # collision time prevents ball getting stuck
        ball.bounce(paddle.location,paddle.position)
        paddle.previousCollisionTime = pg.time.get_ticks()
        print("collided with paddle", paddle.location.name)
  
  def isGameOver():
    global winnerText
    if redScore >= WIN_SCORE:
      winnerText = winnerFont.render("Red Wins!",True,red)
      return True
    elif blueScore >= WIN_SCORE:
      winnerText = winnerFont.render("Blue Wins!",True,blue)
      return True
    return False

  # init elements
  resetScore()
  initElements()

  while True:
    SURF.fill(Colors.BLACK)
    
    if not isGameOver():
      drawScores()
      ball.draw()
      drawPaddles()
      
      keys = pg.key.get_pressed()
      if keys[pg.K_w]: paddleLeft.move(True)
      if keys[pg.K_s]: paddleLeft.move(False)
      if keys[pg.K_a]: paddleDown.move(True)
      if keys[pg.K_d]: paddleDown.move(False)
      if keys[pg.K_UP]: paddleRight.move(True)
      if keys[pg.K_DOWN]: paddleRight.move(False)
      if keys[pg.K_LEFT]: paddleUp.move(True)
      if keys[pg.K_RIGHT]: paddleUp.move(False)
      
      ball.move()
      if ball.isOut(): ball.respawn()
      detectCollision()
    
    else:
      drawGameOver()
    
    for event in pg.event.get():
      if keys[pg.K_ESCAPE]:
          gameState = GameState.MENU
          return
      if event.type == QUIT:
          pg.quit()
          sys.exit()
      if pg.mouse.get_pressed()[0] and gameOverMenuButton.isHovered():
          gameOverMenuButton.pressed()
          return
    pg.display.flip()
    clock.tick(FPS)  

def help():
  global gameState
  helpImage = pg.image.load("help.png")
  help2Image = pg.image.load("help2.png")
  while True:
    SURF.fill(Colors.BLACK)
    
    SURF.blit(helpImage,(WIDTH//2-helpImage.get_width()//2,HEIGHT//5))
    
    keys = pg.key.get_pressed()
    for event in pg.event.get():
      if keys[pg.K_ESCAPE]:
          gameState = GameState.MENU
          return
      if event.type == QUIT:
          pg.quit()
          sys.exit()
    pg.display.flip()
    clock.tick(FPS)  

# main loop
while True:
  if gameState == GameState.MENU:
    title()
  elif gameState == GameState.GAME:
    game()
  elif gameState == GameState.HELP:
    help()