# Lucas Leung
# Pong Graphics Assignment - Pong with a twist
# 3 features:
#   1. Ball stays still and flashes at the start of every round
#   2. On screen countdown timer
#   3. Ball gets faster and faster as the round goes on for longer (1.1x every 3s)

# imports
import sys
import pygame as pg
from pygame.locals import *
from random import randint,choice
from math import radians,cos,sin,atan2
from enum import Enum

# global constants (can be changed to other reasonable values without affecting game)
WINDOW_SIZE = 600
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
def changeState(state:GameState):
  global gameState
  gameState = state

# draw button with text or image that changes the game state
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
    changeState(this.state)

# 4 paddle locations
class PaddleLocation(Enum):
  LEFT=0
  RIGHT=1
  UP=2
  DOWN=3


  # ball

# ball class
class Ball():
  
  DEFAULT_SIZE = 20
  DEFAULT_SPEED = 260/FPS
  FLASH_MS = 1300
  SPEED_INCREASE_FACTOR = 1.1
  SPEED_INCREASE_MS = 3000
  BALL_FILE = "ball.png"
  size = DEFAULT_SIZE
  speed = DEFAULT_SPEED
  
  # random range excludes diagonal corners and angles near perpendicular to paddles
  RANDRANGE = list(range(10,31)) \
            + list(range(60,81)) \
            + list(range(100,121)) \
            + list(range(150,171)) \
            + list(range(190,211)) \
            + list(range(240,261)) \
            + list(range(280,301)) \
            + list(range(330,351))
  
  def __init__(this):
    this.image = pg.transform.smoothscale(pg.image.load(this.BALL_FILE),(this.size,this.size))
    this.angle = radians(this.__genAngle())
    this.rect = this.image.get_rect()
    this.rect.x = randint(WINDOW_SIZE//2-50,WINDOW_SIZE//2+50-this.size)
    this.rect.y = randint(WINDOW_SIZE//2-50,WINDOW_SIZE//2+50-this.size)
    this.mask = pg.mask.from_surface(this.image)
  
  def move(this):
    this.rect.x += this.speed * cos(this.angle)
    this.rect.y += this.speed * sin(this.angle)

  # check if ball hit the wall and changes the score accordingly
  def isOut(this) -> bool:
    global redScore,blueScore
    if this.rect.x<=0:
      blueScore += 1
      return True
    elif this.rect.y<=0:
      redScore += 1
      return True
    elif this.rect.right>=WINDOW_SIZE:
      redScore += 1
      return True
    elif this.rect.bottom>=WINDOW_SIZE:
      blueScore += 1
      return True
    return False
  
  # generate 1 angle from possible angles
  def __genAngle(this) -> int:
    return choice(this.RANDRANGE)
  
  # reset ball size, location, and angle
  def respawn(this):
    this.size = this.DEFAULT_SIZE
    this.rect.topleft = (randint(WINDOW_SIZE//2-50,WINDOW_SIZE//2+50-this.size),randint(WINDOW_SIZE//2-50,WINDOW_SIZE//2+50-this.size))
    this.angle = radians(this.__genAngle())
    this.speed = this.DEFAULT_SPEED
  
  def draw(this):
    SURF.blit(this.image,this.rect)
  
  # change angle of ball based on which paddle the ball hit
  def bounce(this,paddleLocation:PaddleLocation):
    dx = cos(this.angle)
    dy = sin(this.angle)
    match paddleLocation:
      case PaddleLocation.LEFT | PaddleLocation.RIGHT: dx = -dx
      case PaddleLocation.UP | PaddleLocation.DOWN: dy = -dy
    this.angle = atan2(dy,dx)
  
  def changeSize(this,size:int):
    this.size = size
    this.image = pg.transform.smoothscale(pg.image.load(this.BALL_FILE),(this.size,this.size))
    this.rect.update(this.rect.x,this.rect.y,*this.image.get_size())
  
  def increaseSpeed(this):
    this.speed *= this.SPEED_INCREASE_FACTOR

# menu loop
def menu():
  
  def initTitle():
    global titleImage,titleRect
    TITLE_WIDTH = 332
    TITLE_HEIGHT = 102
    titleRect = pg.Rect(WINDOW_SIZE//2-TITLE_WIDTH//2,WINDOW_SIZE//5,TITLE_WIDTH,TITLE_HEIGHT)
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
    playButton = Button(WINDOW_SIZE//2,WINDOW_SIZE//2,MENU_BUTTONS_WIDTH,PLAY_BUTTON_HEIGHT,"play.png",PLAY_BUTTON_BORDER_WIDTH,GameState.GAME,True)
    helpButton = Button(WINDOW_SIZE//2,WINDOW_SIZE*0.7,MENU_BUTTONS_WIDTH,HELP_BUTTON_HEIGHT,"How to play",HELP_BUTTON_BORDER_WIDTH,GameState.HELP,fontSize=26 )
    buttons = (playButton,helpButton)
  
  # bounces the ball on the walls instead of paddles in the menu
  def ballWallBounce():
    if ball.rect.x<=0:
      ball.bounce(PaddleLocation.LEFT)
    elif ball.rect.y<=0:
      ball.bounce(PaddleLocation.UP)
    elif ball.rect.right>=WINDOW_SIZE:
      ball.bounce(PaddleLocation.RIGHT)
    elif ball.rect.bottom>=WINDOW_SIZE:
      ball.bounce(PaddleLocation.DOWN)
    if ball.rect.x<=-10 or ball.rect.y<=-10 or ball.rect.right>=WINDOW_SIZE+10 or ball.rect.bottom>=WINDOW_SIZE+10: # out of bounds for some reason
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
        # random fun thing that makes the menu ball bigger when you click on it
        if ball.rect.collidepoint(pg.mouse.get_pos()):
          print(ball.rect)
          ball.changeSize(ball.size+3)
    
    pg.display.flip()
    clock.tick(FPS)

# game loop
def game():
  
  SCORE_FONT_SIZE = 50
  WIN_SCORE = 10
  MAX_GAME_TIME = 120

  # scores
  def resetScore():
    global redScore,blueScore
    redScore = 0
    blueScore = 0

  # paddle
  class Paddle():
    
    SIZE = WINDOW_SIZE*0.14
    THICKNESS = 10
    PADDING = 10
    SPEED = 520/FPS
    PADDING_SIDE = PADDING*2 # ensures the paddles stop and never overlap each other
    previousCollisionTime = 0
    
    def __init__(this,location:PaddleLocation):
      this.location = location
      match location:
        case PaddleLocation.LEFT:
          this.position = WINDOW_SIZE//2-this.SIZE//2
          this.color = Colors.RED.value
          this.rect = pg.Rect(this.PADDING,this.position,this.THICKNESS,this.SIZE)
          this.mask = pg.mask.Mask((this.THICKNESS,this.SIZE),True)
        case PaddleLocation.RIGHT:
          this.position = WINDOW_SIZE//2-this.SIZE//2
          this.color = Colors.BLUE.value
          this.rect = pg.Rect(WINDOW_SIZE-this.PADDING-this.THICKNESS,this.position,this.THICKNESS,this.SIZE)
          this.mask = pg.mask.Mask((this.THICKNESS,this.SIZE),True)
        case PaddleLocation.UP:
          this.position = WINDOW_SIZE//2-this.SIZE//2
          this.color = Colors.BLUE.value
          this.rect = pg.Rect(this.position,this.PADDING,this.SIZE,this.THICKNESS)
          this.mask = pg.mask.Mask((this.SIZE,this.THICKNESS),True)
        case PaddleLocation.DOWN:
          this.position = WINDOW_SIZE//2-this.SIZE//2
          this.color = Colors.RED.value
          this.rect = pg.Rect(this.position,WINDOW_SIZE-this.PADDING-this.THICKNESS,this.SIZE,this.THICKNESS)
          this.mask = pg.mask.Mask((this.SIZE,this.THICKNESS),True)
    
    def _update(this):
      match this.location:
        case PaddleLocation.LEFT: this.rect.update(this.PADDING,this.position,this.THICKNESS,this.SIZE)
        case PaddleLocation.RIGHT: this.rect.update(WINDOW_SIZE-this.PADDING-this.THICKNESS,this.position,this.THICKNESS,this.SIZE)
        case PaddleLocation.UP: this.rect.update(this.position,this.PADDING,this.SIZE,this.THICKNESS)
        case PaddleLocation.DOWN: this.rect.update(this.position,WINDOW_SIZE-this.PADDING-this.THICKNESS,this.SIZE,this.THICKNESS)
    
    def draw(this):
      pg.draw.rect(SURF,this.color,this.rect)
    
    # move paddle based on true or false
    def move(this,direction:bool):
      if direction:
        this.position -= min(this.SPEED,this.position-this.PADDING_SIDE)
      else:
        match this.location:
          case PaddleLocation.LEFT | PaddleLocation.RIGHT:
            this.position += min(this.SPEED,WINDOW_SIZE-this.position-this.SIZE-this.PADDING_SIDE)
          case PaddleLocation.UP | PaddleLocation.DOWN:
            this.position += min(this.SPEED,WINDOW_SIZE-this.position-this.SIZE-this.PADDING_SIDE)
      this._update()
  
  # draw scores
  def drawScores():
    redScoreRender = font.render(str(redScore),True,Colors.WHITE.value)
    blueScoreRender = font.render(str(blueScore),True,Colors.WHITE.value)
    SURF.blit(redScoreRender,(WINDOW_SIZE*0.1,WINDOW_SIZE//2-redScoreRender.get_height()//2))
    SURF.blit(blueScoreRender,(WINDOW_SIZE-(WINDOW_SIZE*0.1+blueScoreRender.get_width()),WINDOW_SIZE//2-blueScoreRender.get_height()//2))

  # draw timer
  def drawTimer():
    m,s = divmod(MAX_GAME_TIME-(gameTime//1000),60)
    timestr = f"{m}:{s:02d}"
    timestrRender = font.render(timestr,True,Colors.WHITE.value)
    SURF.blit(timestrRender,(WINDOW_SIZE//2-timestrRender.get_width()//2,WINDOW_SIZE//2-timestrRender.get_height()//2))

  # draw game over screen
  def drawGameOver():
    SURF.blit(gameOverText,(WINDOW_SIZE//2-gameOverText.get_width()//2,WINDOW_SIZE*0.2))
    winnerTextRender = renderWinnerText()
    SURF.blit(winnerTextRender,(WINDOW_SIZE//2-winnerTextRender.get_width()//2,WINDOW_SIZE*0.4))
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
    paddles=(paddleLeft,paddleRight,paddleUp,paddleDown)
    font = pg.font.Font(FONT_FILE,SCORE_FONT_SIZE)
    winnerFont = pg.font.Font(FONT_FILE,WINNER_FONT_SIZE)
    gameOverText = font.render("Game Over",True,Colors.WHITE.value)
    gameOverMenuButton = Button(WINDOW_SIZE//2,WINDOW_SIZE*0.6,GAME_OVER_BUTTON_WIDTH,GAME_OVER_BUTTON_HEIGHT,"MENU",GAME_OVER_BUTTON_BORDER_WIDTH,GameState.MENU)

  def detectCollision():
    for paddle in paddles:
      offset = paddle.rect.x - ball.rect.x, paddle.rect.y - ball.rect.y
      if ball.mask.overlap(paddle.mask,offset) and pg.time.get_ticks() - paddle.previousCollisionTime > 200:
        # collision time prevents ball getting stuck
        ball.bounce(paddle.location)
        paddle.previousCollisionTime = pg.time.get_ticks()
  
  def renderWinnerText() -> pg.surface.Surface:
    if redScore > blueScore:
      return winnerFont.render("Red Wins!",True,Colors.RED.value)
    elif blueScore > redScore:
      return winnerFont.render("Blue Wins!",True,Colors.BLUE.value)
    else:
      return winnerFont.render("Tie!",True,Colors.WHITE.value)
  
  def isGameOver() -> bool:
    return redScore >= WIN_SCORE or blueScore >= WIN_SCORE

  # init elements
  resetScore()
  initElements()
  pg.time.set_timer(101,ball.SPEED_INCREASE_MS) # timer for speed increase
  pg.time.set_timer(102,100) # round time
  roundTime = 0
  gameTime = 0
  
  while True:
    SURF.fill(Colors.BLACK.value)
    keys = pg.key.get_pressed()
    
    if isGameOver() or gameTime >= MAX_GAME_TIME*1000:
      drawGameOver()
    else:
      drawScores()
      drawTimer()
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
      if roundTime > ball.FLASH_MS:
        ball.draw()
        ball.move()
      elif roundTime % 500 < 300: # the ball is shown for 300ms for every 500ms
        ball.draw()
      
      # reset ball when out
      if ball.isOut():
        ball.respawn()
        pg.time.set_timer(102,100)
        roundTime = 0 # reset round time when new round starts
      
      # detect if ball is hitting paddle
      detectCollision()

    for event in pg.event.get():
      if event.type == QUIT:
          pg.quit()
          sys.exit()
      if isGameOver() and pg.mouse.get_pressed()[0] and gameOverMenuButton.isHovered():
        gameOverMenuButton.pressed()
        return
      if keys[pg.K_ESCAPE]:
          changeState(GameState.MENU)
          return
      if event.type == 101 and roundTime > ball.FLASH_MS:
        ball.increaseSpeed()
      if event.type == 102:
        roundTime += 100
        if roundTime > ball.FLASH_MS: gameTime += 100 # don't increment game time when the ball is flashing

    pg.display.flip()
    clock.tick(FPS)  

# help loop
def help():

  HELP_IMAGE_FILE = "help.png"
  HELP2_IMAGE_FILE = "help2.png"
  
  helpImage = pg.transform.smoothscale(pg.image.load(HELP_IMAGE_FILE),(WINDOW_SIZE*0.936,WINDOW_SIZE*0.243))
  help2Image = pg.transform.smoothscale(pg.image.load(HELP2_IMAGE_FILE),(WINDOW_SIZE*0.929,WINDOW_SIZE*0.262))
  
  while True:
    SURF.fill(Colors.BLACK.value)
    
    # draw instruction text
    SURF.blit(helpImage,(WINDOW_SIZE//2-helpImage.get_width()//2,WINDOW_SIZE*0.2))
    SURF.blit(help2Image,(WINDOW_SIZE//2-help2Image.get_width()//2,WINDOW_SIZE*0.25+helpImage.get_height()))
    
    keys = pg.key.get_pressed()
    for event in pg.event.get():
      if keys[pg.K_ESCAPE]:
        changeState(GameState.MENU)
        return
      if event.type == QUIT:
        pg.quit()
        sys.exit()

    pg.display.flip()
    clock.tick(FPS)  

# main function
def main():
  global SURF,clock
  # pygame init
  pg.init()
  SURF = pg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
  pg.display.set_caption('Pong with a Twist!')
  clock = pg.time.Clock()
  changeState(GameState.MENU)

  # main loop
  while True:
    match gameState:
      case GameState.MENU: menu()
      case GameState.GAME: game()
      case GameState.HELP: help()

main()