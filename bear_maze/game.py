import pygame
from PIL import Image, ImageEnhance
import os
import math
from bear_maze.maze import mazes
# from spelling_bee.game import SpellingBeeGame

SCREEN_HEIGHT = 1080
SCREEN_WIDTH = 1920
FONT_SIZE = 24
FPS = 60
LEVEL = mazes
COLOR = "chartreuse3"
SECONDARY_COLOR = "chartreuse4"
COLOR2 = "black"
PI = math.pi
BEAR_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/bear_still.png'), (45,45))
GRASS_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/grass_block.png'), (64,32))
GRASS = 0
CAVE_SIGN_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/cave_sign.png'), (64,32))
CAVE_SIGN = 2
ARROW_UP_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/w_arrow.png'), (64,32))
DARK_ARROW_UP_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/dark_w_arrow.png'), (64,32))
ARROW_UP = 3
ARROW_RIGHT_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/d_arrow.png'), (64,32))
DARK_ARROW_RIGHT_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/dark_d_arrow.png'), (64,32))
ARROW_RIGHT = 4
ARROW_DOWN_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/s_arrow.png'), (64,32))
DARK_ARROW_DOWN_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/dark_s_arrow.png'), (64,32))
ARROW_DOWN = 5
ARROW_LEFT_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/a_arrow.png'), (64,32))
DARK_ARROW_LEFT_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/dark_a_arrow.png'), (64,32))
ARROW_LEFT = 6
OBSTACLE = 1
UP = 2
RIGHT = 0
DOWN = 3
LEFT = 1
LEFT_MOUSE_BUTTON = 0
CENTER_ADJUSTMENT = 23
BEAR_START_X = 450
BEAR_START_Y = 300
TILE_HEIGHT = ((SCREEN_HEIGHT  - 50) // 32) # = 32
TILE_WIDTH = (SCREEN_WIDTH // 30) # = 64
C9_FUDGE_FACTOR = 32
BEAR_SPEED = 8
BRIGHTNESS_FACTOR = 0.5

ENEMY_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/bee.png'), (30,30))

class BearMazeGame:
  def __init__(self, number_of_bees, number_of_honey_jars): 
    pygame.init()
    self.screen_width = SCREEN_HEIGHT
    self.screen_height = SCREEN_WIDTH
    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    self.timer = pygame.time.Clock()
    self.running = True
    self.bear_x = BEAR_START_X
    self.bear_y = BEAR_START_Y
    # Starting direction for bear
    self.direction = RIGHT
    # Order will always be U, L, R, D
    self.clickable_arrow_keys = []
    self.goal_tile = []
    self.number_of_bees = number_of_bees
    self.number_of_honey_jars = number_of_honey_jars
    # self.load_assests()  

  def load_assests(self):
    print("load assets") 
    # raw_image = pygame.image.load(os.path.join("assests", "images", "background.png"))
    # self.background_image = pygame.transform.scale(raw_image, (self.screen_width, self.screen_height))
    # self.font = pygame.font.Font(os.path.join("assests", "fonts", "OpenSans-Regular.ttf"), FONT_SIZE)
  
  def draw_maze(self, level):
    for i in range(len(level)):
      for j in range(len(level[i])):
        if level[i][j] == GRASS:
          self.screen.blit(GRASS_IMAGE, (j * TILE_WIDTH, i * TILE_HEIGHT))
        elif level[i][j] == CAVE_SIGN:
          self.screen.blit(CAVE_SIGN_IMAGE, (j * TILE_WIDTH, i * TILE_HEIGHT))
          self.goal_tile.append(pygame.Rect((j * TILE_WIDTH, i * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)))
        elif level[i][j] == ARROW_UP:
           self.screen.blit(ARROW_UP_IMAGE, (j * TILE_WIDTH, i * TILE_HEIGHT))
           self.clickable_arrow_keys.append(pygame.Rect((j * TILE_WIDTH, i * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)))
        elif level[i][j] == ARROW_RIGHT:
           self.screen.blit(ARROW_RIGHT_IMAGE, (j * TILE_WIDTH, i * TILE_HEIGHT))
           self.clickable_arrow_keys.append(pygame.Rect((j * TILE_WIDTH, i * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)))
        elif level[i][j] == ARROW_DOWN:
           self.screen.blit(ARROW_DOWN_IMAGE, (j * TILE_WIDTH, i * TILE_HEIGHT))
           self.clickable_arrow_keys.append(pygame.Rect((j * TILE_WIDTH, i * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)))
        elif level[i][j] == ARROW_LEFT:
            self.screen.blit(ARROW_LEFT_IMAGE, (j * TILE_WIDTH, i * TILE_HEIGHT))
            self.clickable_arrow_keys.append(pygame.Rect((j * TILE_WIDTH, i * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)))
        else:
          pygame.draw.rect(self.screen, COLOR2, pygame.Rect((j * TILE_WIDTH, i * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)))
  
  def draw_bear(self):
    self.screen.blit(BEAR_IMAGE, (self.bear_x, self.bear_y))

  def draw_enemies(self):
    self.screen.blit(ENEMY_IMAGE, (self.bear_x + 150, self.bear_y))
    
  def end_game(self, game_state):
    if game_state == "won":
      print("you win")
    elif game_state == "lost":
      print("you lose")
    
  def check_position(self, level):
    # R, L, U, D
    turns = [False, False, False, False]
    if self.goal_tile[0].collidepoint(self.center_x, self.center_y):
      self.end_game("won")
    if self.center_x // TILE_WIDTH < 30 and self.center_x // TILE_WIDTH > 1:
      # If you're currently moving RIGHT, you should be able to move LEFT, back to your initial position
      if self.direction == RIGHT:
        if level[self.center_y // TILE_HEIGHT][(self.center_x - TILE_WIDTH) // TILE_WIDTH] != OBSTACLE:
          turns[1] = True
      # If you're currently moving LEFT, you should be able to move RIGHT, back to your initial position
      if self.direction == LEFT:
        if level[self.center_y // TILE_HEIGHT][(self.center_x + TILE_WIDTH) // TILE_WIDTH] != OBSTACLE:
          turns[0] = True
      # If you're currently moving UP, you should be able to move DOWN, back to your initial position
      if self.direction == UP:
        if level[(self.center_y + TILE_HEIGHT) // TILE_HEIGHT][self.center_x // TILE_WIDTH] != OBSTACLE:
          turns[3] = True
      # If you're currently moving DOWN, you should be able to move UP, back to your initial position
      if self.direction == DOWN:
        if level[(self.center_y - TILE_HEIGHT) // TILE_HEIGHT][self.center_x // TILE_WIDTH] != OBSTACLE:
          turns[2] = True

      if self.direction == UP or self.direction == DOWN:
        if level[(self.center_y + C9_FUDGE_FACTOR) // TILE_HEIGHT][self.center_x // TILE_WIDTH] != OBSTACLE:
          turns[3] = True
        if level[(self.center_y - C9_FUDGE_FACTOR) // TILE_HEIGHT][self.center_x // TILE_WIDTH] != OBSTACLE:
          turns[2] = True
        if level[self.center_y // TILE_HEIGHT][(self.center_x - TILE_WIDTH) // TILE_WIDTH] != OBSTACLE:
          turns[1] = True
        if level[self.center_y // TILE_HEIGHT][(self.center_x + TILE_WIDTH) // TILE_WIDTH] != OBSTACLE:
          turns[0] = True

      if self.direction == RIGHT or self.direction == LEFT:
        if level[(self.center_y + TILE_HEIGHT) // TILE_HEIGHT][self.center_x // TILE_WIDTH] != OBSTACLE:
          turns[3] = True
        if level[(self.center_y - TILE_HEIGHT) // TILE_HEIGHT][self.center_x // TILE_WIDTH] != OBSTACLE:
          turns[2] = True
        if level[self.center_y // TILE_HEIGHT][(self.center_x - C9_FUDGE_FACTOR) // TILE_WIDTH] != OBSTACLE:
          turns[1] = True
        if level[self.center_y // TILE_HEIGHT][(self.center_x + C9_FUDGE_FACTOR) // TILE_WIDTH] != OBSTACLE:
          turns[0] = True
    else:
      turns[0] = True
      turns[1] = True
    return turns

  def move_bear(self, bear_x, bear_y, turns_allowed):
    if self.direction == RIGHT and turns_allowed[0]:
      bear_x += BEAR_SPEED
    elif self.direction == LEFT and turns_allowed[1]:
      bear_x -= BEAR_SPEED
    elif self.direction == UP and turns_allowed[2]:
      bear_y -= BEAR_SPEED
    elif self.direction == DOWN and turns_allowed[3]:
      bear_y += BEAR_SPEED
    return bear_x, bear_y
    
  def run(self):
    while self.running:
      direction = None
      self.timer.tick(FPS)
      self.screen.fill(COLOR)
      self.draw_maze(LEVEL)
      self.draw_bear()
      self.draw_enemies()
      self.center_x = self.bear_x + CENTER_ADJUSTMENT
      self.center_y = self.bear_y + CENTER_ADJUSTMENT
      turns_allowed = self.check_position(LEVEL)
      for event in pygame.event.get():
        if event.type == pygame.QUIT: 
          self.running = False
      
      keys = pygame.key.get_pressed()
      if keys[pygame.K_w]:
        self.screen.blit(DARK_ARROW_UP_IMAGE, (self.clickable_arrow_keys[0].left, self.clickable_arrow_keys[0].top))
        direction = UP
      if keys[pygame.K_a]:
        self.screen.blit(DARK_ARROW_LEFT_IMAGE, (self.clickable_arrow_keys[1].left, self.clickable_arrow_keys[1].top))
        direction = LEFT
      if keys[pygame.K_d]:
        self.screen.blit(DARK_ARROW_RIGHT_IMAGE, (self.clickable_arrow_keys[2].left, self.clickable_arrow_keys[2].top))
        direction = RIGHT
      if keys[pygame.K_s]:
        self.screen.blit(DARK_ARROW_DOWN_IMAGE, (self.clickable_arrow_keys[3].left, self.clickable_arrow_keys[3].top))
        direction = DOWN
      
      mouse = pygame.mouse.get_pressed()
      if mouse[LEFT_MOUSE_BUTTON]:
        position = pygame.mouse.get_pos()
        if self.clickable_arrow_keys[0].collidepoint(position):
          self.screen.blit(DARK_ARROW_UP_IMAGE, (self.clickable_arrow_keys[0].left, self.clickable_arrow_keys[0].top))
          direction = UP
        elif self.clickable_arrow_keys[1].collidepoint(position):
          self.screen.blit(DARK_ARROW_LEFT_IMAGE, (self.clickable_arrow_keys[1].left, self.clickable_arrow_keys[1].top))
          direction = LEFT
        elif self.clickable_arrow_keys[2].collidepoint(position):
          self.screen.blit(DARK_ARROW_RIGHT_IMAGE, (self.clickable_arrow_keys[2].left, self.clickable_arrow_keys[2].top))
          direction = RIGHT
        elif self.clickable_arrow_keys[3].collidepoint(position):
          self.screen.blit(DARK_ARROW_DOWN_IMAGE, (self.clickable_arrow_keys[3].left, self.clickable_arrow_keys[3].top))
          direction = DOWN

      for i in range(len(turns_allowed)):
        if direction == i and turns_allowed[i]:
          self.direction = i
          self.bear_x, self.bear_y = self.move_bear(self.bear_x, self.bear_y, turns_allowed)

      pygame.display.flip()
    
    pygame.quit()
