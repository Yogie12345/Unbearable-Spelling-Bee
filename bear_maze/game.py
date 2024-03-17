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
COLOR2 = "black"
PI = math.pi
BEAR_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/bear_still.png'), (45,45))
GRASS_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/grass_block.png'), (64,32))
CAVE_SIGN_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/cave_sign.png'), (64,32))
ARROW_UP_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/w_arrow.png'), (64,32))
ARROW_RIGHT_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/d_arrow.png'), (64,32))
ARROW_DOWN_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/s_arrow.png'), (64,32))
ARROW_LEFT_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/a_arrow.png'), (64,32))
BEAR_START_X = 450
BEAR_START_Y = 300
TILE_HEIGHT = ((SCREEN_HEIGHT  - 50) // 32) # = 32
TILE_WIDTH = (SCREEN_WIDTH // 30) # = 64
C9_FUDGE_FACTOR = 32
BEAR_SPEED = 8

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
        if level[i][j] == 0:
          self.screen.blit(GRASS_IMAGE, (j * TILE_WIDTH, i * TILE_HEIGHT))
        elif level[i][j] == 2:
          self.screen.blit(CAVE_SIGN_IMAGE, (j * TILE_WIDTH, i * TILE_HEIGHT))
        elif level[i][j] == 3:
           self.screen.blit(ARROW_UP_IMAGE, (j * TILE_WIDTH, i * TILE_HEIGHT))
        elif level[i][j] == 4:
           self.screen.blit(ARROW_RIGHT_IMAGE, (j * TILE_WIDTH, i * TILE_HEIGHT))
        elif level[i][j] == 5:
           self.screen.blit(ARROW_DOWN_IMAGE, (j * TILE_WIDTH, i * TILE_HEIGHT))
        elif level[i][j] == 6:
            self.screen.blit(ARROW_LEFT_IMAGE, (j * TILE_WIDTH, i * TILE_HEIGHT))
        else:
          pygame.draw.rect(self.screen, COLOR2, pygame.Rect((j * TILE_WIDTH, i * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)))
  
  def draw_bear(self):
    self.screen.blit(BEAR_IMAGE, (self.bear_x, self.bear_y))
    
  def check_position(self, level):
    # R, L, U, D
    turns = [False, False, False, False]
    if self.center_x // TILE_WIDTH < 30 and self.center_x // TILE_WIDTH > 1:
      # If you're currently moving RIGHT, you should be able to move LEFT, back to your initial position
      if self.direction == 0:
        if level[self.center_y // TILE_HEIGHT][(self.center_x - TILE_WIDTH) // TILE_WIDTH] != 1:
          turns[1] = True
      # If you're currently moving LEFT, you should be able to move RIGHT, back to your initial position
      if self.direction == 1:
        if level[self.center_y // TILE_HEIGHT][(self.center_x + TILE_WIDTH) // TILE_WIDTH] != 1:
          turns[0] = True
      # If you're currently moving UP, you should be able to move DOWN, back to your initial position
      if self.direction == 2:
        if level[(self.center_y + TILE_HEIGHT) // TILE_HEIGHT][self.center_x // TILE_WIDTH] != 1:
          turns[3] = True
      # If you're currently moving DOWN, you should be able to move UP, back to your initial position
      if self.direction == 3:
        if level[(self.center_y - TILE_HEIGHT) // TILE_HEIGHT][self.center_x // TILE_WIDTH] != 1:
          turns[2] = True

      if self.direction == 2 or self.direction == 3:
        if level[(self.center_y + C9_FUDGE_FACTOR) // TILE_HEIGHT][self.center_x // TILE_WIDTH] != 1:
          turns[3] = True
        if level[(self.center_y - C9_FUDGE_FACTOR) // TILE_HEIGHT][self.center_x // TILE_WIDTH] != 1:
          turns[2] = True
        if level[self.center_y // TILE_HEIGHT][(self.center_x - TILE_WIDTH) // TILE_WIDTH] != 1:
          turns[1] = True
        if level[self.center_y // TILE_HEIGHT][(self.center_x + TILE_WIDTH) // TILE_WIDTH] != 1:
          turns[0] = True

      if self.direction == 0 or self.direction == 1:
        if level[(self.center_y + TILE_HEIGHT) // TILE_HEIGHT][self.center_x // TILE_WIDTH] != 1:
          turns[3] = True
        if level[(self.center_y - TILE_HEIGHT) // TILE_HEIGHT][self.center_x // TILE_WIDTH] != 1:
          turns[2] = True
        if level[self.center_y // TILE_HEIGHT][(self.center_x - C9_FUDGE_FACTOR) // TILE_WIDTH] != 1:
          turns[1] = True
        if level[self.center_y // TILE_HEIGHT][(self.center_x + C9_FUDGE_FACTOR) // TILE_WIDTH] != 1:
          turns[0] = True
    else:
      turns[0] = True
      turns[1] = True
    return turns

  def move_bear(self, bear_x, bear_y, turns_allowed):
    if self.direction == 0 and turns_allowed[0]:
      bear_x += BEAR_SPEED
    elif self.direction == 1 and turns_allowed[1]:
      bear_x -= BEAR_SPEED
    elif self.direction == 2 and turns_allowed[2]:
      bear_y -= BEAR_SPEED
    elif self.direction == 3 and turns_allowed[3]:
      bear_y += BEAR_SPEED
    return bear_x, bear_y
    
  def run(self):
    while self.running:
      direction = -1
      self.timer.tick(FPS)
      self.screen.fill(COLOR)
      self.draw_maze(LEVEL)
      self.draw_bear()
      self.center_x = self.bear_x + 23
      self.center_y = self.bear_y + 23
      turns_allowed = self.check_position(LEVEL)
      for event in pygame.event.get():
        if event.type == pygame.QUIT: 
          self.running = False
    
      keys = pygame.key.get_pressed()
      if keys[pygame.K_a]:
        direction = 1
      if keys[pygame.K_w]:
        direction = 2
      if keys[pygame.K_d]:
        direction = 0
      if keys[pygame.K_s]:
        direction = 3

      for i in range(len(turns_allowed)):
        if direction == i and turns_allowed[i]:
          self.direction = i
          self.bear_x, self.bear_y = self.move_bear(self.bear_x, self.bear_y, turns_allowed)

      pygame.display.flip()
    
    pygame.quit()
