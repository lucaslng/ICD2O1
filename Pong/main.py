from enum import Enum
import sys
import pygame as pg
from pygame.locals import *
import random as rand
import math

# global constants
WIDTH = 600
HEIGHT = 600
FPS = 30
FONT_FILE = "font.ttf"

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
def changeState(state=GameState.MENU):
  global gameState
  gameState = state

# pygame init
pg.init()
SURF = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Pong with a Twist!')
clock = pg.time.Clock()

# draw button with text or image
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
      this.blit = pg.transform.smoothscale(pg.image.load(text),this.innerRect.size)
      this.blitRect = this.innerRect
    else:
      this.font = pg.font.Font(FONT_FILE,this.fontSize)
      this.blit = this.font.render(text,True,Colors.WHITE.value)
      this.blitRect = pg.Rect((this.innerRect.width-this.blit.get_width())//2+this.innerRect.x,((this.innerRect.height-this.blit.get_height())//2)+this.innerRect.y,*this.blit.get_size())
  
  def isHovered(this) -> bool:
    return this.rect.collidepoint(pg.mouse.get_pos())
  
  def draw(this):
    if this.isHovered():
      pg.draw.rect(SURF,Colors.WHITE.value,this.rect)
    else:
      pg.draw.rect(SURF,Colors.GRAY.value,this.rect)
    pg.draw.rect(SURF,Colors.BLACK.value,this.innerRect)
    SURF.blit(this.blit,this.blitRect.topleft)
  
  def pressed(this):
    print(this.state.name, "button pressed")
    changeState(this.state)

class PaddleLocation(Enum):
  LEFT=0
  RIGHT=1
  UP=2
  DOWN=3
    
  # ball
class Ball():
  
  DEFAULT_SIZE = 20
  size = DEFAULT_SIZE
  SPEED = 260/FPS
  randrange = list(range(10,31)) + list(range(60,81)) + list(range(100,121)) + list(range(150,171)) + list(range(190,211)) + list(range(240,261)) + list(range(280,301)) + list(range(330,351))
  
  def __init__(this):
    this.image = pg.transform.smoothscale(pg.image.load("ball.png"),(this.size,this.size))
    this.angle = math.radians(this._genAngle())
    this.rect = this.image.get_rect()
    this.rect.x = rand.randint(WIDTH//2-50,WIDTH//2+50-this.size)
    this.rect.y = rand.randint(HEIGHT//2-50,HEIGHT//2+50-this.size)
    this.mask = pg.mask.from_surface(this.image)
    
  def move(this):
    this.rect.x += this.SPEED * math.cos(this.angle)
    this.rect.y += this.SPEED * math.sin(this.angle)

  def isOut(this) -> bool:
    global redScore,blueScore
    if this.rect.x<=0:
      blueScore += 1
      return True
    elif this.rect.y<=0:
      redScore += 1
      return True
    elif this.rect.right>=WIDTH:
      redScore += 1
      return True
    elif this.rect.bottom>=HEIGHT:
      blueScore += 1
      return True
    return False
  
  def _genAngle(this) -> int:
    return rand.choice(this.randrange)
  
  def respawn(this):
    this.size = this.DEFAULT_SIZE
    this.rect.topleft = (rand.randint(WIDTH//2-50,WIDTH//2+50-this.size),rand.randint(HEIGHT//2-50,HEIGHT//2+50-this.size))
    this.angle = math.radians(this._genAngle())
  
  def draw(this):
    SURF.blit(this.image,this.rect)
  
  def bounce(this,paddleLocation:PaddleLocation):
    dx = math.cos(this.angle)
    dy = math.sin(this.angle)
    if paddleLocation == PaddleLocation.LEFT or paddleLocation == PaddleLocation.RIGHT:
      dx = -dx
    elif paddleLocation == PaddleLocation.UP or paddleLocation == PaddleLocation.DOWN:
      dy = -dy
    else:
      print("Unknown paddle location", paddleLocation, "when bouncing")
    this.angle = math.atan2(dy,dx)
  
  def changeSize(this,size:int):
    this.size = size
    this.image = pg.transform.smoothscale(pg.image.load("ball.png"),(this.size,this.size))
    this.rect.update(this.rect.x,this.rect.y,*this.image.get_size())


# menu loop
def menu():
  
  def initTitle():
    global titleImage,titleRect
    TITLE_WIDTH = 332
    TITLE_HEIGHT = 102
    titleRect = pg.Rect(WIDTH//2-TITLE_WIDTH//2,HEIGHT//5,TITLE_WIDTH,TITLE_HEIGHT)
    titleImage = pg.transform.smoothscale(pg.image.load("title.png"),(TITLE_WIDTH,TITLE_HEIGHT))
  
  def drawTitle():
    SURF.blit(titleImage,titleRect)
  
  def initButtons():
    global buttons,playButton,helpButton
    MENU_BUTTONS_WIDTH = 320
    PLAY_BUTTON_HEIGHT = 102
    PLAY_BUTTON_BORDER_WIDTH = 10
    HELP_BUTTON_HEIGHT = 80
    HELP_BUTTON_BORDER_WIDTH = 10
    playButton = Button(WIDTH//2,HEIGHT//2,MENU_BUTTONS_WIDTH,PLAY_BUTTON_HEIGHT,"play.png",PLAY_BUTTON_BORDER_WIDTH,GameState.GAME,True)
    helpButton = Button(WIDTH//2,HEIGHT*0.7,MENU_BUTTONS_WIDTH,HELP_BUTTON_HEIGHT,"How to play",HELP_BUTTON_BORDER_WIDTH,GameState.HELP,fontSize=26 )
    buttons = (playButton,helpButton)
  
  def ballWallBounce():
    if ball.rect.x<=0:
      ball.bounce(PaddleLocation.LEFT)
    elif ball.rect.y<=0:
      ball.bounce(PaddleLocation.UP)
    elif ball.rect.right>=WIDTH:
      ball.bounce(PaddleLocation.RIGHT)
    elif ball.rect.bottom>=HEIGHT:
      ball.bounce(PaddleLocation.DOWN)
    if ball.rect.x<=-10 or ball.rect.y<=-10 or ball.rect.right>=WIDTH+10 or ball.rect.bottom>=HEIGHT+10:
      ball.respawn()
        
  initTitle()
  initButtons()
  ball = Ball()
  
  while True:
    SURF.fill(Colors.BLACK.value)
    
    ball.draw()
    drawTitle()
    playButton.draw()
    helpButton.draw()
    
    ball.move()
    ballWallBounce()
    
    for event in pg.event.get():
      if event.type == QUIT:
        pg.quit()
        sys.exit()
      if pg.mouse.get_pressed()[0]:
        
        for button in buttons:
          if button.isHovered():
            button.pressed()
            return
        if ball.rect.collidepoint(pg.mouse.get_pos()):
          print(ball.rect)
          ball.changeSize(ball.size+3)
    
    pg.display.flip()
    clock.tick(FPS)

# game loop
def game():
  
  SCORE_FONT_SIZE = 50

  # scores
  def resetScore():
    global redScore,blueScore
    redScore = 0
    blueScore = 0

  # paddle
  class Paddle():
    
    SIZE = 70
    THICKNESS = 10
    PADDING = 10
    SPEED = 520/FPS
    PADDING_SIDE = 14
    previousCollisionTime = 0
    
    def __init__(this,location:PaddleLocation):
      this.location = location
      if location == PaddleLocation.LEFT:
        this.position = HEIGHT//2-this.SIZE//2
        this.color = Colors.RED.value
        this.rect = pg.Rect(this.PADDING,this.position,this.THICKNESS,this.SIZE)
        this
        this.mask = pg.mask.Mask((this.THICKNESS,this.SIZE),True)
      elif location == PaddleLocation.RIGHT:
        this.position = HEIGHT//2-this.SIZE//2
        this.color = Colors.BLUE.value
        this.rect = pg.Rect(WIDTH-this.PADDING-this.THICKNESS,this.position,this.THICKNESS,this.SIZE)
        this.mask = pg.mask.Mask((this.THICKNESS,this.SIZE),True)
      elif location == PaddleLocation.UP:
        this.position = WIDTH//2-this.SIZE//2
        this.color = Colors.BLUE.value
        this.rect = pg.Rect(this.position,this.PADDING,this.SIZE,this.THICKNESS)
        this.mask = pg.mask.Mask((this.SIZE,this.THICKNESS),True)
      elif location == PaddleLocation.DOWN:
        this.position = WIDTH//2-this.SIZE//2
        this.color = Colors.RED.value
        this.rect = pg.Rect(this.position,HEIGHT-this.PADDING-this.THICKNESS,this.SIZE,this.THICKNESS)
        this.mask = pg.mask.Mask((this.SIZE,this.THICKNESS),True)
    
    def _update(this):
      if this.location == PaddleLocation.LEFT: this.rect = pg.Rect(this.PADDING,this.position,this.THICKNESS,this.SIZE)
      elif this.location == PaddleLocation.RIGHT: this.rect = pg.Rect(WIDTH-this.PADDING-this.THICKNESS,this.position,this.THICKNESS,this.SIZE)
      elif this.location == PaddleLocation.UP: this.rect = pg.Rect(this.position,this.PADDING,this.SIZE,this.THICKNESS)
      elif this.location == PaddleLocation.DOWN: this.rect = pg.Rect(this.position,HEIGHT-this.PADDING-this.THICKNESS,this.SIZE,this.THICKNESS)
    
    def draw(this):
      pg.draw.rect(SURF,this.color,this.rect)
    
    def move(this,direction:bool):
      if direction:
        this.position -= min(this.SPEED,this.position-this.PADDING_SIDE)
      else:
        if this.location == PaddleLocation.LEFT or this.location == PaddleLocation.RIGHT:
          this.position += min(this.SPEED,HEIGHT-this.position-this.SIZE-this.PADDING_SIDE)
        else:
          this.position += min(this.SPEED,WIDTH-this.position-this.SIZE-this.PADDING_SIDE)
      this._update()
  
  # draw scores
  def drawScores():
    SURF.blit(font.render(str(redScore),True,Colors.WHITE.value),(WIDTH*0.1,HEIGHT//2-SCORE_FONT_SIZE//2))
    SURF.blit(font.render(str(blueScore),True,Colors.WHITE.value),(WIDTH*0.8,HEIGHT//2-SCORE_FONT_SIZE//2))

# draw game over screen
  def drawGameOver():
    SURF.blit(gameOverText,(WIDTH//2-gameOverText.get_width()//2,HEIGHT*0.2))
    SURF.blit(winnerText,(WIDTH//2-winnerText.get_width()//2,HEIGHT*0.4))
    gameOverMenuButton.draw()
  
  # element functions
  def drawPaddles():
    for paddle in paddles:
      paddle.draw()

  def initElements():
    global paddleLeft,paddleRight,paddleUp,paddleDown,paddles,ball,font,winnerFont,gameOverText,gameOverMenuButton
    WINNER_FONT_SIZE = 40
    GAME_OVER_BUTTON_WIDTH = 280
    GAME_OVER_BUTTON_HEIGHT = 90
    GAME_OVER_BUTTON_BORDER_WIDTH = 10
    paddleLeft = Paddle(PaddleLocation.LEFT)
    paddleRight = Paddle(PaddleLocation.RIGHT)
    paddleUp = Paddle(PaddleLocation.UP)
    paddleDown = Paddle(PaddleLocation.DOWN)
    ball = Ball()
    paddles=[paddleLeft,paddleRight,paddleUp,paddleDown]
    font = pg.font.Font(FONT_FILE,SCORE_FONT_SIZE)
    winnerFont = pg.font.Font(FONT_FILE,WINNER_FONT_SIZE)
    gameOverText = font.render("Game Over",True,Colors.WHITE.value)
    gameOverMenuButton = Button(WIDTH//2,HEIGHT*0.6,GAME_OVER_BUTTON_WIDTH,GAME_OVER_BUTTON_HEIGHT,"MENU",GAME_OVER_BUTTON_BORDER_WIDTH,GameState.MENU)

  def detectCollision():
    for paddle in paddles:
      offset = paddle.rect.x - ball.rect.x, paddle.rect.y - ball.rect.y
      if ball.mask.overlap(paddle.mask,offset) and pg.time.get_ticks() - paddle.previousCollisionTime > 180:
        # collision time prevents ball getting stuck
        ball.bounce(paddle.location)
        paddle.previousCollisionTime = pg.time.get_ticks()
  
  def isGameOver() -> bool:
    global winnerText
    WIN_SCORE = 10
    if redScore >= WIN_SCORE:
      winnerText = winnerFont.render("Red Wins!",True,Colors.RED.value)
      return True
    elif blueScore >= WIN_SCORE:
      winnerText = winnerFont.render("Blue Wins!",True,Colors.BLUE.value)
      return True
    return False

  # init elements
  resetScore()
  initElements()
  flashingTime = pg.time.get_ticks() + 500 # flash for longer on first round
  
  while True:
    SURF.fill(Colors.BLACK.value)
    keys = pg.key.get_pressed()
    
    if not isGameOver():
      drawScores()
      drawPaddles()
      
      if keys[pg.K_w]: paddleLeft.move(True)
      if keys[pg.K_s]: paddleLeft.move(False)
      if keys[pg.K_a]: paddleDown.move(True)
      if keys[pg.K_d]: paddleDown.move(False)
      if keys[pg.K_UP]: paddleRight.move(True)
      if keys[pg.K_DOWN]: paddleRight.move(False)
      if keys[pg.K_LEFT]: paddleUp.move(True)
      if keys[pg.K_RIGHT]: paddleUp.move(False)
      
      # if ball just respawned, flash the ball
      if pg.time.get_ticks() - flashingTime > 1300:
        ball.draw()
        ball.move()
      elif (pg.time.get_ticks() - flashingTime) % 500 < 300: # the ball is shown for 300ms for every 500ms
        ball.draw()
      
      # reset ball when out
      if ball.isOut():
        ball.respawn()
        flashingTime = pg.time.get_ticks()
      
      # detect if ball is hitting paddle
      detectCollision()
    
    else: # game over
      drawGameOver()
    
    for event in pg.event.get():
      if pg.mouse.get_pressed()[0] and gameOverMenuButton.isHovered():
        gameOverMenuButton.pressed()
        return
      if keys[pg.K_ESCAPE]:
          changeState()
          return
      if event.type == QUIT:
          pg.quit()
          sys.exit()

    pg.display.flip()
    clock.tick(FPS)  

# help loop
def help():
  HELP_IMAGE_FILE = "help.png"
  HELP2_IMAGE_FILE = "help2.png"
  
  helpImage = pg.transform.smoothscale(pg.image.load(HELP_IMAGE_FILE),(WIDTH*0.936,HEIGHT*0.243))
  help2Image = pg.transform.smoothscale(pg.image.load(HELP2_IMAGE_FILE),(WIDTH*0.929,HEIGHT*0.262))
  
  while True:
    SURF.fill(Colors.BLACK.value)
    
    SURF.blit(helpImage,(WIDTH//2-helpImage.get_width()//2,HEIGHT*0.2))
    SURF.blit(help2Image,(WIDTH//2-help2Image.get_width()//2,HEIGHT*0.25+helpImage.get_height()))
    
    keys = pg.key.get_pressed()
    for event in pg.event.get():
      if keys[pg.K_ESCAPE]:
        changeState()
        return
      if event.type == QUIT:
        pg.quit()
        sys.exit()

    pg.display.flip()
    clock.tick(FPS)  

# main loop
while True:
  if gameState == GameState.MENU:
    menu()
  elif gameState == GameState.GAME:
    game()
  elif gameState == GameState.HELP:
    help()
  else:
    print("Unknown game state", gameState, "exiting")
    pg.quit()
    sys.exit()