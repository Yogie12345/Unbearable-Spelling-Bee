import pygame
import os
import math
from bear_maze.maze import mazes

SCREEN_HEIGHT = 1080
SCREEN_WIDTH = 1920
FONT_SIZE = 24
FPS = 60
LEVEL = mazes
COLOR = "green"
PI = math.pi
BEAR_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/bear_still.png'), (80,80))
BEAR_START_X = 450
BEAR_START_Y = 250
TILE_HEIGHT = ((SCREEN_HEIGHT  - 50) // 32)
TILE_WIDTH = (SCREEN_WIDTH // 30)
C9_FUDGE_FACTOR = 15

class BearMazeGame:
  def __init__(self): 
    pygame.init()
    self.screen_width = SCREEN_HEIGHT
    self.screen_height = SCREEN_WIDTH
    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    self.timer = pygame.time.Clock()
    self.running = True
    self.bear_x = BEAR_START_X
    self.bear_y = BEAR_START_Y
    self.can_turn = [False, False, False, False]
    self.direction = 0
    # self.load_assests()  
    # self.initialize_game()

  def load_assests(self):
    print("load assets") 
    # raw_image = pygame.image.load(os.path.join("assests", "images", "background.png"))
    # self.background_image = pygame.transform.scale(raw_image, (self.screen_width, self.screen_height))
    # self.font = pygame.font.Font(os.path.join("assests", "fonts", "OpenSans-Regular.ttf"), FONT_SIZE)
  
  def draw_maze(self, level):
    for i in range(len(level)):
      for j in range(len(level[i])):
        if level[i][j] == 1:
          pygame.draw.line(self.screen, COLOR, (j * TILE_WIDTH + (0.5 * TILE_WIDTH), i * TILE_HEIGHT), 
                          (j * TILE_WIDTH + (0.5 * TILE_WIDTH), i * TILE_HEIGHT + TILE_HEIGHT), 3)
        if level[i][j] == 2:
          pygame.draw.line(self.screen, COLOR, (j * TILE_WIDTH, i * TILE_HEIGHT + (0.5 * TILE_HEIGHT)), 
                        (j * TILE_WIDTH + TILE_WIDTH, i * TILE_HEIGHT + (0.5 * TILE_HEIGHT)), 3)
        if level[i][j] == 3:
          pygame.draw.arc(self.screen, COLOR, 
                          [(j * TILE_WIDTH + (0.5 * TILE_WIDTH)), (i * TILE_HEIGHT + (0.5 * TILE_HEIGHT)), TILE_WIDTH, TILE_HEIGHT], PI/2, PI, 3)
        if level[i][j] == 4:
          pygame.draw.arc(self.screen, COLOR, 
                          [(j * TILE_WIDTH - (0.4 * TILE_WIDTH)) - 2, (i * TILE_HEIGHT + (0.5 * TILE_HEIGHT)), TILE_WIDTH, TILE_HEIGHT], 0, PI/2, 3)
        # if level[i][j] == 5:
        if level[i][j] == 6:
          pygame.draw.arc(self.screen, COLOR, 
                          [(j * TILE_WIDTH + (0.5 * TILE_WIDTH)), (i * TILE_HEIGHT - (0.4 * TILE_HEIGHT)), TILE_WIDTH, TILE_HEIGHT], PI, 3*PI/2, 3)
        if level[i][j] == 7:
          pygame.draw.arc(self.screen, COLOR, 
                          [(j * TILE_WIDTH - (0.4 * TILE_WIDTH)) - 2, (i * TILE_HEIGHT - (0.4 * TILE_HEIGHT)), TILE_WIDTH, TILE_HEIGHT], 3*PI/2, 2*PI, 3)
        if level[i][j] == 8:
          pygame.draw.rect(self.screen, COLOR, pygame.Rect((j * TILE_WIDTH, i * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)))
  
  def draw_bear(self):
    self.screen.blit(BEAR_IMAGE, (self.bear_x, self.bear_y))
    
  def check_position(self, level):
    turns = [False, False, False, False]

    if self.center_x // 30 < 29:
      if self.direction == 0:
        if level[self.center_y // TILE_HEIGHT][(self.center_x - C9_FUDGE_FACTOR) // TILE_WIDTH] < 3:
          turns[1] = True
      if self.direction == 1:
        if level[self.center_y // TILE_HEIGHT][(self.center_x + C9_FUDGE_FACTOR) // TILE_WIDTH] < 3:
          turns[0] = True
      if self.direction == 2:
        if level[(self.center_y + C9_FUDGE_FACTOR) // TILE_HEIGHT][self.center_x // TILE_WIDTH] < 3:
          turns[3] = True
      if self.direction == 3:
        if level[(self.center_y - C9_FUDGE_FACTOR) // TILE_HEIGHT][self.center_x // TILE_WIDTH] < 3:
          turns[2] = True
      
      if self.direction == 2 or self.direction == 3:
        if 12 <= self.center_x % TILE_WIDTH <= 18:
          if level[(self.center_y + C9_FUDGE_FACTOR) // TILE_HEIGHT][self.center_x // TILE_WIDTH] < 3:
            turns[3] = True
          if level[(self.center_y - C9_FUDGE_FACTOR) // TILE_HEIGHT][self.center_x // TILE_WIDTH] < 3:
            turns[2] = True
        if 12 <= self.center_x % TILE_HEIGHT <= 18:
          if level[self.center_y // TILE_HEIGHT][(self.center_x - TILE_WIDTH) // TILE_WIDTH] < 3:
            turns[1] = True
          if level[self.center_y// TILE_HEIGHT][(self.center_x + TILE_WIDTH) // TILE_WIDTH] < 3:
            turns[0] = True
      
      if self.direction == 0 or self.direction == 1:
        if 12 <= self.center_x % TILE_WIDTH <= 18:
          if level[(self.center_y + TILE_HEIGHT) // TILE_HEIGHT][self.center_x // TILE_WIDTH] < 3:
            turns[3] = True
          if level[(self.center_y - TILE_HEIGHT) // TILE_HEIGHT][self.center_x // TILE_WIDTH] < 3:
            turns[2] = True
        if 12 <= self.center_x % TILE_HEIGHT <= 18:
          if level[self.center_y // TILE_HEIGHT][(self.center_x - C9_FUDGE_FACTOR) // TILE_WIDTH] < 3:
            turns[1] = True
          if level[self.center_y// TILE_HEIGHT][(self.center_x + C9_FUDGE_FACTOR) // TILE_WIDTH] < 3:
            turns[0] = True
    else:
      turns[0] = True
      turns[1] = True
    
    return turns

  def run(self):
    while self.running: 
      self.timer.tick(FPS)
      self.screen.fill("black")
      self.draw_maze(LEVEL)
      self.draw_bear()
      self.center_x = self.bear_x + 23
      self.center_y = self.bear_y + 23
      turns_allowed = self.check_position(LEVEL)
      for event in pygame.event.get():
        if event.type == pygame.QUIT: 
          self.running = False
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_LEFT:
            self.direction = 1
          if event.key == pygame.K_UP:
            self.direction = 2
          if event.key == pygame.K_RIGHT:
            self.direction = 0
          if event.key == pygame.K_DOWN:
            self.direction = 3

        for i in range(len(turns_allowed)):
          if self.direction == i and turns_allowed[i]:
            self.direction = 1


      pygame.display.flip()
    
    pygame.quit()
