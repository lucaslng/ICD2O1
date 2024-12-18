# Lucas Leung
# Bridge Word Guessing Game
# This is a game where you guess the letters in a word.
# I'm not really sure if I should disable a letter after a wrong guess is made
# or after the player has guessed every instance of that letter in the word
# but I did the former because that makes it a little more difficult

import sys
import pygame as pg
from pygame.locals import *
from random import choice, randint

pg.init()
clock = pg.time.Clock()
WIDTH = 1000
HEIGHT = 800
SURF = pg.display.set_mode((WIDTH, HEIGHT))
FRAME = SURF.get_rect()
FPS = 60

ALPHA = "abcdefghijklmnopqrstuvwxyz"

white = (255, 255, 255)
black = (0, 0, 0)
hoveredGray = (220, 220, 220)
disabledGray = (100, 100, 100)

state = "menu"

words = (
    "semantically",
    "rendezvous",
    "projects",
    "launchpad",
    "bookkeeper",
    "barracudas",
    "unequivocally",
    "inconsequential",
    "juxtaposition",
    "doppelganger",
  )

LETTER_BUTTON_SIZE = 40
LETTER_PADDING = 10

font140 = pg.font.Font(None, 140)
font80 = pg.font.Font(None, 80)
font40 = pg.font.Font(None, 40)
hanging40 = pg.font.Font("hanging.ttf", 40)
hanging80 = pg.font.Font("hanging.ttf", 80)
hanging140 = pg.font.Font("hanging.ttf", 140)

reloadIcon = pg.transform.smoothscale(pg.image.load("reload.png").convert_alpha(), (30, 30))

exitButtonRect = pg.rect.Rect(FRAME.right - LETTER_BUTTON_SIZE - LETTER_PADDING, FRAME.top + LETTER_PADDING, LETTER_BUTTON_SIZE, LETTER_BUTTON_SIZE)
exitText = font40.render("X", True, black)
def drawExitButton():
  if exitButtonRect.collidepoint(pg.mouse.get_pos()):
    pg.draw.rect(SURF, hoveredGray, exitButtonRect, border_radius=3)
  pg.draw.rect(SURF, black, exitButtonRect, 2, 3)
  SURF.blit(exitText, (exitButtonRect.centerx - exitText.get_width() // 2, exitButtonRect.centery - exitText.get_height() // 2))
  

def menu():
  '''Menu screen'''
  
  titleText = hanging140.render("Bridge Game", True, black)
  playText = font140.render("PLAY", True, black)
  playButtonRect = pg.rect.Rect(FRAME.centerx - playText.get_width() -10, FRAME.height * 0.6, playText.get_width() * 2, playText.get_height()*1.2)
  while True:
    SURF.fill(white)
    
    SURF.blit(titleText, (FRAME.centerx - titleText.get_width() // 2, FRAME.height * 0.2))
    
    
    if playButtonRect.collidepoint(pg.mouse.get_pos()):
      pg.draw.rect(SURF, hoveredGray, playButtonRect, border_radius=4)
    pg.draw.rect(SURF, black, playButtonRect, 3, 4)
    SURF.blit(playText, (playButtonRect.centerx - playText.get_width() // 2, playButtonRect.centery - playText.get_height() // 2))
    drawExitButton()
    
    keys = pg.key.get_pressed()
    for event in pg.event.get():
      if event.type == QUIT:
        pg.quit()
        sys.exit()
      if pg.mouse.get_pressed()[0]:
        if playButtonRect.collidepoint(pg.mouse.get_pos()):
          return "game"
        if exitButtonRect.collidepoint(pg.mouse.get_pos()):
          pg.quit()
          sys.exit()
    
    pg.display.flip()
    clock.tick(FPS)


def game():
  '''Game screen'''
  global word, collapse, bridge, guesses, step, guessedLetters, lives
  
  word = choice(words)
  length = len(word)
  lives = randint(4, 8)
  guesses = "_" * length
  collapse = length
  bridge = "-" * length
  guess = ""
  guessedLetters = ""
  
  step = 0
  
  letterButtons = [pg.rect.Rect( \
                      ((FRAME.right - 13 * (LETTER_BUTTON_SIZE + LETTER_PADDING)) / 2 + (i * (LETTER_BUTTON_SIZE + LETTER_PADDING) if i < 13 else (i - 13) * (LETTER_BUTTON_SIZE + LETTER_PADDING))),
                      FRAME.height * 0.8 if i < 13 else FRAME.height * 0.8 + (LETTER_BUTTON_SIZE + LETTER_PADDING),
                      LETTER_BUTTON_SIZE,
                      LETTER_BUTTON_SIZE,
                    )
                   for i in range(26)]
  
  
  def doGuess(guess: str) -> str:
    '''Perform a guess based on the letter guessed'''
    global word, collapse, bridge, guesses, step, guessedLetters, lives
    if word.find(guess) != -1:
      guesses = guesses[:word.find(guess)] + guess + guesses[word.find(guess)+1:]
      word = word[:word.find(guess)] + "*" + word[word.find(guess)+1:]
      step += 1
      if step == len(word):
        return "win"
    else:
      guessedLetters += guess
      collapse -= 1
      lives -= 1
      bridge = bridge[:collapse] + "#"+ bridge[collapse+1:]
      if lives <= 0:
        return "lose"
    return "continue"
  
  restartButtonRect = pg.rect.Rect(FRAME.right - 2 * (LETTER_BUTTON_SIZE + LETTER_PADDING), FRAME.top + LETTER_PADDING, LETTER_BUTTON_SIZE, LETTER_BUTTON_SIZE)
  restartText = font40.render("⟳", True, black)
  
  while True:
    SURF.fill(white)
    
    for event in pg.event.get():
      if event.type == QUIT:
        pg.quit()
        sys.exit()
      if event.type == pg.KEYDOWN:
        guess = pg.key.name(event.key).lower()
        if guess in ALPHA and guess not in guessedLetters: # doing .isalpha() includes space so I did this instead
          guessResult = doGuess(guess)
          if guessResult != "continue":
            return guessResult
        else: guess = ""
      if pg.mouse.get_pressed()[0]:
        if exitButtonRect.collidepoint(pg.mouse.get_pos()):
          pg.quit()
          sys.exit()
        if restartButtonRect.collidepoint(pg.mouse.get_pos()):
          return "game"
      for i in range(len(letterButtons)):
        if pg.mouse.get_pressed()[0] and letterButtons[i].collidepoint(pg.mouse.get_pos()):
          guess = ALPHA[i]
          if guess not in guessedLetters:
            guessResult = doGuess(guess)
            if guessResult != "continue":
              return guessResult
          else: guess = ""
    
    guessLetterText = font80.render(("Guess a letter: " + guess), True, black)
    SURF.blit(guessLetterText, ((FRAME.right - 13 * (LETTER_BUTTON_SIZE + LETTER_PADDING)) / 2, FRAME.height * 0.7))
    
    for i in range(len(letterButtons)):
      if ALPHA[i] in guessedLetters:
        pg.draw.rect(SURF, disabledGray, letterButtons[i], border_radius=3)
      elif letterButtons[i].collidepoint(pg.mouse.get_pos()):
        pg.draw.rect(SURF, hoveredGray, letterButtons[i], border_radius=3)
      pg.draw.rect(SURF, black, letterButtons[i], 2, 3)
      letter = font40.render(ALPHA[i].upper(), True, black)
      SURF.blit(letter, (letterButtons[i].centerx - letter.get_width() // 2, letterButtons[i].centery - letter.get_height() // 2))

    
    livesText = font80.render(("Lives: " + str(lives)), True, black)
    guessesText = hanging80.render(guesses, True, black)
    bridgeText = hanging80.render(bridge, True, black)
    personText = font80.render(((step * " ") + "X"), True, black)
    SURF.blit(livesText, ((FRAME.left + 120) / 2, FRAME.height * 0.1))
    SURF.blit(personText, (FRAME.centerx - bridgeText.get_width() // 2, FRAME.height * 0.2))
    SURF.blit(bridgeText, (FRAME.centerx - bridgeText.get_width() // 2, FRAME.height * 0.3))
    SURF.blit(guessesText, (FRAME.centerx - guessesText.get_width() // 2, FRAME.height * 0.5))
    pg.draw.polygon(SURF, black, points = (
                    (FRAME.centerx - bridgeText.get_width() // 2 - 10, FRAME.height * 0.37),
                    (FRAME.centerx - bridgeText.get_width() // 2 - 10, FRAME.height * 0.42),
                    (FRAME.centerx - bridgeText.get_width() // 2 - 80, FRAME.height * 0.42),
                  ), width = 2)
    pg.draw.polygon(SURF, black, points = (
                    (FRAME.centerx + bridgeText.get_width() // 2 + 10, FRAME.height * 0.37),
                    (FRAME.centerx + bridgeText.get_width() // 2 + 10, FRAME.height * 0.42),
                    (FRAME.centerx + bridgeText.get_width() // 2 + 80, FRAME.height * 0.42),
                  ), width = 2)

    if restartButtonRect.collidepoint(pg.mouse.get_pos()):
      pg.draw.rect(SURF, hoveredGray, restartButtonRect, border_radius=3)
    pg.draw.rect(SURF, black, restartButtonRect, 2, 3)
    SURF.blit(reloadIcon, (restartButtonRect.centerx - 30 // 2, restartButtonRect.centery - 30 // 2))
  
    drawExitButton()
    
    pg.display.flip()
    clock.tick()

def end():
  '''End screen'''
  if state == "win":
    text = hanging140.render("YOU WON!", True, black)
  else:
    text = hanging140.render("YOU LOSE!", True, black)
  
  playText = font140.render("PLAY AGAIN", True, black)
  playButtonRect = pg.rect.Rect(FRAME.centerx - playText.get_width() // 2 - 20, FRAME.height * 0.5, playText.get_width() + 40, playText.get_height()*1.2)
  menuText = font140.render("MENU", True, black)
  menuButtonRect = playButtonRect.copy()
  menuButtonRect.y = playButtonRect.bottom + 20
  
  while True:
    SURF.fill(white)
    
    SURF.blit(text, (FRAME.centerx - text.get_width() // 2, FRAME.height * 0.25))
    
    if playButtonRect.collidepoint(pg.mouse.get_pos()):
      pg.draw.rect(SURF, hoveredGray, playButtonRect, border_radius=4)
    elif menuButtonRect.collidepoint(pg.mouse.get_pos()):
      pg.draw.rect(SURF, hoveredGray, menuButtonRect, border_radius=4)
    pg.draw.rect(SURF, black, playButtonRect, 3, 4)
    pg.draw.rect(SURF, black, menuButtonRect, 3, 4)
    SURF.blit(playText, (playButtonRect.centerx - playText.get_width() // 2, playButtonRect.centery - playText.get_height() // 2))
    SURF.blit(menuText, (menuButtonRect.centerx - menuText.get_width() // 2, menuButtonRect.centery - menuText.get_height() // 2))
    
    drawExitButton()
    
    for event in pg.event.get():
      if event.type == QUIT:
        pg.quit()
        sys.exit()
      if pg.mouse.get_pressed()[0]:
        if exitButtonRect.collidepoint(pg.mouse.get_pos()):
          pg.quit()
          sys.exit()
        if playButtonRect.collidepoint(pg.mouse.get_pos()):
          return "game"
        if menuButtonRect.collidepoint(pg.mouse.get_pos()):
          return "menu"
    
    pg.display.flip()
    clock.tick(FPS)

# each screen simply returns the next state
while True:
  if state == "menu":
    state = menu()
  elif state == "game":
    state = game()
  elif state == "win" or state == "lose":
    state = end()