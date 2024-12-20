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
  global changedWord, collapse, bridge, guesses, step, guessedLetters
  
  word = choice(words) # random word out of list
  changedWord = word # the word will be changed throughout the program to remember the guessed letters
  length = len(changedWord) # length of word
  difficulty = randint(4, 8) # number of incorrect answers allowed
  guesses = "_" * length # show the letters the player has guessed
  collapse = difficulty # the index where the bridge is collapsed, starts at the end of the bridge (no tiles collapsed)
  bridge = "-" * difficulty # show the bridge
  guess = "" # the player's guess
  guessedLetters = "" # store the letters the player has guessed
  step = 0 # the position the player is at
  
  # create letter button rects in two rows
  letterButtons = [pg.rect.Rect( \
                      ((FRAME.right - 13 * (LETTER_BUTTON_SIZE + LETTER_PADDING)) / 2 + (i * (LETTER_BUTTON_SIZE + LETTER_PADDING) if i < 13 else (i - 13) * (LETTER_BUTTON_SIZE + LETTER_PADDING))),
                      FRAME.height * 0.8 if i < 13 else FRAME.height * 0.8 + (LETTER_BUTTON_SIZE + LETTER_PADDING),
                      LETTER_BUTTON_SIZE,
                      LETTER_BUTTON_SIZE,
                    )
                   for i in range(26)]
  
  
  def doGuess(guess: str) -> str:
    '''Perform a guess based on the letter guessed'''
    global changedWord, collapse, bridge, guesses, step, guessedLetters, lives
    if changedWord.find(guess) != -1:
      guesses = guesses[:changedWord.find(guess)] + guess + guesses[changedWord.find(guess)+1:]
      changedWord = changedWord[:changedWord.find(guess)] + "*" + changedWord[changedWord.find(guess)+1:]
      step += (difficulty + 2) / len(changedWord) * LETTER_BUTTON_SIZE # add two before diving to include the start and end position of the player
      if step >= (difficulty + 2) * LETTER_BUTTON_SIZE:
        return "win"
    else:
      guessedLetters += guess
      collapse -= 1
      bridge = bridge[:collapse] + "#"+ bridge[collapse+1:]
      if collapse <= 0:
        return "lose"
    return "continue"
  
  restartButtonRect = pg.rect.Rect(FRAME.right - 2 * (LETTER_BUTTON_SIZE + LETTER_PADDING), FRAME.top + LETTER_PADDING, LETTER_BUTTON_SIZE, LETTER_BUTTON_SIZE)
  
  textBoxButtonRect = pg.rect.Rect((FRAME.right - 13 * (LETTER_BUTTON_SIZE + LETTER_PADDING)) / 2,
                                  FRAME.height * 0.65,
                                  13 * (LETTER_BUTTON_SIZE + LETTER_PADDING),
                                  90
                      )
  isTyping = False
  typedStr = ""
  guessWordButtonRect = pg.rect.Rect(
    (FRAME.centerx + 13 * (LETTER_BUTTON_SIZE + LETTER_PADDING) / 2) - LETTER_BUTTON_SIZE * 2 - LETTER_PADDING / 2,
    FRAME.height * 0.65 + LETTER_PADDING / 2,
    LETTER_BUTTON_SIZE * 2,
    LETTER_BUTTON_SIZE * 2,
  )
  guessWordButtonIcon = font80.render("->", True, black)
  
  while True:
    SURF.fill(white)
    
    for event in pg.event.get():
      if event.type == QUIT:
        pg.quit()
        sys.exit()
      if event.type == pg.KEYDOWN:
        guess = pg.key.name(event.key).lower()
        if guess in ALPHA:
          if isTyping:
            if len(typedStr) < 16:
              typedStr += guess
          elif guess not in guessedLetters: # doing .isalpha() includes space so I did this instead
            guessResult = doGuess(guess)
            if guessResult != "continue":
              return guessResult
        if isTyping:
          if guess == "backspace":
            typedStr = typedStr[:-1]
          elif guess == "return":
            print(typedStr, word)
            if typedStr == word:
              return "win"
            else:
              collapse -= 1
              bridge = bridge[:collapse] + "#"+ bridge[collapse+1:]
              if collapse <= 0:
                return "lose"
      
      clickedButton = False
      if pg.mouse.get_pressed()[0]:
        if exitButtonRect.collidepoint(pg.mouse.get_pos()):
          pg.quit()
          sys.exit()
        elif restartButtonRect.collidepoint(pg.mouse.get_pos()):
          return "game"
        elif guessWordButtonRect.collidepoint(pg.mouse.get_pos()):
          clickedButton = True
          if typedStr != "":
            if typedStr == word:
              return "win"
            else:
              collapse -= 1
              bridge = bridge[:collapse] + "#"+ bridge[collapse+1:]
              if collapse <= 0:
                return "lose"
          typedStr = ""
        elif textBoxButtonRect.collidepoint(pg.mouse.get_pos()):
          isTyping = True
          clickedButton = True
        for i in range(len(letterButtons)):
          if letterButtons[i].collidepoint(pg.mouse.get_pos()):
            clickedButton = True
            guess = ALPHA[i]
            if isTyping:
              if len(typedStr) < 16:
                typedStr += guess
            else:
              if guess not in guessedLetters:
                guessResult = doGuess(guess)
                if guessResult != "continue":
                  return guessResult
              else: guess = ""
        if not clickedButton:
          typedStr = ""
          isTyping = False
    
    # draw textbox
    if (textBoxButtonRect.collidepoint(pg.mouse.get_pos()) and not guessWordButtonRect.collidepoint(pg.mouse.get_pos())) or isTyping:
      pg.draw.rect(SURF, hoveredGray, textBoxButtonRect, border_radius=4)
    pg.draw.rect(SURF, black, textBoxButtonRect, 3, 4)
    if not isTyping:
      guessLetterText = font80.render(("Guess the word"), True, disabledGray)
    else:
      guessLetterText = font80.render((typedStr), True, black)
    SURF.blit(guessLetterText, (textBoxButtonRect.left + 20, textBoxButtonRect.top + guessLetterText.get_height() // 2))
    
    if guessWordButtonRect.collidepoint(pg.mouse.get_pos()):
      pg.draw.rect(SURF, hoveredGray, guessWordButtonRect, border_radius=4)
    else:
      pg.draw.rect(SURF, white, guessWordButtonRect, border_radius=4)
    pg.draw.rect(SURF, black, guessWordButtonRect, 3, 4)
    SURF.blit(guessWordButtonIcon, (guessWordButtonRect.left + LETTER_PADDING * 2, guessWordButtonRect.top + LETTER_PADDING))
    
    
    # draw letter buttons
    for i in range(len(letterButtons)):
      if ALPHA[i] in guessedLetters:
        pg.draw.rect(SURF, disabledGray, letterButtons[i], border_radius=3)
      elif letterButtons[i].collidepoint(pg.mouse.get_pos()):
        pg.draw.rect(SURF, hoveredGray, letterButtons[i], border_radius=3)
      pg.draw.rect(SURF, black, letterButtons[i], 2, 3)
      letter = font40.render(ALPHA[i].upper(), True, black)
      SURF.blit(letter, (letterButtons[i].centerx - letter.get_width() // 2, letterButtons[i].centery - letter.get_height() // 2))

    # draw person and bridge
    personText = font80.render("X", True, black)
    bridgeStartPos = FRAME.centerx - difficulty * LETTER_BUTTON_SIZE // 2
    bridgeEndPos = FRAME.centerx + difficulty * LETTER_BUTTON_SIZE // 2
    SURF.blit(personText, (bridgeStartPos + step - LETTER_BUTTON_SIZE, FRAME.height * 0.2))
    
    # draw each character in the bridge separately because the characters have different width
    for i in range(difficulty):
      bridgeCharacter = hanging80.render(bridge[i], True, black)
      SURF.blit(bridgeCharacter, (bridgeStartPos + i * LETTER_BUTTON_SIZE, FRAME.height * 0.3))
    for i in range(length):
      guessesCharacter = hanging80.render(guesses[i], True, black)
      SURF.blit(guessesCharacter, (i * LETTER_BUTTON_SIZE*1.5 + FRAME.centerx - (length * LETTER_BUTTON_SIZE * 1.5 / 2), FRAME.height * 0.5))
    
    # triangles at the end of the bridge
    pg.draw.polygon(SURF, black, points = (
                    (bridgeStartPos - 10, FRAME.height * 0.37),
                    (bridgeStartPos - 10, FRAME.height * 0.42),
                    (bridgeStartPos - 80, FRAME.height * 0.42),
                  ), width = 2)
    pg.draw.polygon(SURF, black, points = (
                    (bridgeEndPos + 10, FRAME.height * 0.37),
                    (bridgeEndPos + 10, FRAME.height * 0.42),
                    (bridgeEndPos + 80, FRAME.height * 0.42),
                  ), width = 2)

    # restart and exit buttons
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