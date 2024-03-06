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

class BearMazeGame:
  def __init__(self): 
    pygame.init()
    self.screen_width = SCREEN_HEIGHT
    self.screen_height = SCREEN_WIDTH
    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    self.timer = pygame.time.Clock()
    self.running = True
    # self.load_assests()  
    # self.initialize_game()

  def load_assests(self):
    print("load assets") 
    # raw_image = pygame.image.load(os.path.join("assests", "images", "background.png"))
    # self.background_image = pygame.transform.scale(raw_image, (self.screen_width, self.screen_height))
    # self.font = pygame.font.Font(os.path.join("assests", "fonts", "OpenSans-Regular.ttf"), FONT_SIZE)
  
  def draw_maze(self, level):
    tile_height = ((SCREEN_HEIGHT  - 50) // 32)
    tile_width = (SCREEN_WIDTH // 30)
    for i in range(len(level)):
      for j in range(len(level[i])):
        if level[i][j] == 1:
          pygame.draw.line(self.screen, COLOR, (j * tile_width + (0.5 * tile_width), i * tile_height), 
                          (j * tile_width + (0.5 * tile_width), i * tile_height + tile_height), 3)
        if level[i][j] == 2:
          pygame.draw.line(self.screen, COLOR, (j * tile_width, i * tile_height + (0.5 * tile_height)), 
                        (j * tile_width + tile_width, i * tile_height + (0.5 * tile_height)), 3)
        if level[i][j] == 3:
          pygame.draw.arc(self.screen, COLOR, 
                          [(j * tile_width + (0.5 * tile_width)), (i * tile_height + (0.5 * tile_height)), tile_width, tile_height], PI/2, PI, 3)
        if level[i][j] == 4:
          pygame.draw.arc(self.screen, COLOR, 
                          [(j * tile_width - (0.4 * tile_width)) - 2, (i * tile_height + (0.5 * tile_height)), tile_width, tile_height], 0, PI/2, 3)
        # if level[i][j] == 5:
        if level[i][j] == 6:
          pygame.draw.arc(self.screen, COLOR, 
                          [(j * tile_width + (0.5 * tile_width)), (i * tile_height - (0.4 * tile_height)), tile_width, tile_height], PI, 3*PI/2, 3)
        if level[i][j] == 7:
          pygame.draw.arc(self.screen, COLOR, 
                          [(j * tile_width - (0.4 * tile_width)) - 2, (i * tile_height - (0.4 * tile_height)), tile_width, tile_height], 3*PI/2, 2*PI, 3)
        if level[i][j] == 8:
          pygame.draw.rect(self.screen, COLOR, pygame.Rect((j * tile_width, i * tile_height, tile_width, tile_height)))

  def run(self):
    while self.running: 
      self.timer.tick(FPS)
      self.screen.fill("black")
      self.draw_maze(LEVEL)
      for event in pygame.event.get():
        if event.type == pygame.QUIT: 
          self.running = False


      pygame.display.flip()
    
    pygame.quit()
