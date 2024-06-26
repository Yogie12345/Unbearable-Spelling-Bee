import pygame
import math
from bear_maze.maze import mazes
import random
import time

SCREEN_HEIGHT = 1080
SCREEN_WIDTH = 1920
FONT_SIZE = 36
FPS = 60
LEVEL = mazes
COLOR = "chartreuse3"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GOLD = (255, 215, 0)
RED = (255, 0, 0)
PI = math.pi
BEAR_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/bear_still.png'), (45,45))
TUTORIAL_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/tutorial.png'), (1000,600))
HELP_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/help.png'), (60,60))
ANGRY_BEAR_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/angry_bear.png'), (45,45))
MINUS_ONE_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/minus_one.png'), (45,45))
GRASS_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/grass_block.png'), (64,32))
GRASS = 0
V1_ROCK_OBSTACLE_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/rock_obstacle_1.png'), (64,32))
V2_ROCK_OBSTACLE_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/rock_obstacle_2.png'), (64,32))
V3_ROCK_OBSTACLE_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/rock_obstacle_3.png'), (64,32))
BUSH_OBSTACLE_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/bush_obstacle_1.png'), (64,32))
WOOD_LOG_OBSTACLE_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/wood_log_obstacle.png'), (64,32))
V1_ROCK_OBSTACLE = 7
V2_ROCK_OBSTACLE = 8
V3_ROCK_OBSTACLE = 9
BUSH_OBSTACLE = 10
WOOD_LOG_OBSTACLE = 11
MENU_SCREEN = 12
OBSTACLE = [V1_ROCK_OBSTACLE, V2_ROCK_OBSTACLE, V3_ROCK_OBSTACLE, BUSH_OBSTACLE, WOOD_LOG_OBSTACLE]
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
BEAR_SPEED = 10
BEE_SPEED = 7
ENEMY_IMAGE = pygame.transform.scale(pygame.image.load(f'assets/images/maze_images/angry_bee.png'), (30,30))
FLIPPED_ENEMY_IMAGE = pygame.transform.flip(ENEMY_IMAGE, True, False)
MINIMUM_NUMBER_OF_BEES = 3
MAXIMUM_NUMBER_OF_BEES = 8
class Bee:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.speed = BEE_SPEED
    self.movingRight = True  # Initialize moving direction

  def move(self):
    # Check if the object should move right
    if self.movingRight:
      # Check if the object is within the right limit
      if self.x < SCREEN_WIDTH - 450:
        self.x += self.speed  # Move right
      else:
        self.movingRight = False  # Change direction to left
    else:
      # Check if the object is within the left limit
      if self.x > 350:
        self.x -= self.speed  # Move left
      else:
        self.movingRight = True  # Change direction to right

class BearMazeGame:
  def __init__(self, number_of_bees, number_of_honey_jars, total_number_of_honey): 
    pygame.init()
    self.screen_width = SCREEN_HEIGHT
    self.screen_height = SCREEN_WIDTH
    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    self.timer = pygame.time.Clock()
    self.maze_running = True
    self.bear_x = BEAR_START_X
    self.bear_y = BEAR_START_Y
    # Starting direction for bear
    self.direction = RIGHT
    # Order will always be U, L, R, D
    self.clickable_arrow_keys = []
    self.goal_tile = []
    if (MINIMUM_NUMBER_OF_BEES + number_of_bees) > MAXIMUM_NUMBER_OF_BEES:
      self.number_of_bees = MAXIMUM_NUMBER_OF_BEES
    else:
      self.number_of_bees = MINIMUM_NUMBER_OF_BEES + number_of_bees
    self.number_of_honey_jars = number_of_honey_jars
    # List to hold bee objects
    self.bees = []
    # Spawn bees at initial position
    self.create_bees(self.number_of_bees)
    # Create Rect object for bear
    self.bear_rect = pygame.Rect(self.bear_x, self.bear_y, BEAR_IMAGE.get_width(), BEAR_IMAGE.get_height())
    # Create Rect objects for bees
    self.bee_rects = [pygame.Rect(bee.x, bee.y, ENEMY_IMAGE.get_width(), ENEMY_IMAGE.get_height()) for bee in self.bees]
    self.angry_timer = 0
    self.angry_duration = 3
    self.total_number_of_honey = total_number_of_honey
    

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
        elif level[i][j] == V1_ROCK_OBSTACLE:
          self.screen.blit(V1_ROCK_OBSTACLE_IMAGE, (j * TILE_WIDTH, i * TILE_HEIGHT))
        elif level[i][j] == V2_ROCK_OBSTACLE:
          self.screen.blit(V2_ROCK_OBSTACLE_IMAGE, (j * TILE_WIDTH, i * TILE_HEIGHT))
        elif level[i][j] == V3_ROCK_OBSTACLE:
          self.screen.blit(V3_ROCK_OBSTACLE_IMAGE, (j * TILE_WIDTH, i * TILE_HEIGHT))
        elif level[i][j] == BUSH_OBSTACLE:
          self.screen.blit(BUSH_OBSTACLE_IMAGE, (j * TILE_WIDTH, i * TILE_HEIGHT))
        elif level[i][j] == WOOD_LOG_OBSTACLE:
          self.screen.blit(WOOD_LOG_OBSTACLE_IMAGE, (j * TILE_WIDTH, i * TILE_HEIGHT))
        elif level[i][j] == MENU_SCREEN:
          pygame.draw.rect(self.screen, BLACK, pygame.Rect((j * TILE_WIDTH, i * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)))

  def draw_bear(self):
    if time.time() - self.angry_timer < self.angry_duration:
      self.screen.blit(MINUS_ONE_IMAGE, (self.bear_x + 35, self.bear_y - MINUS_ONE_IMAGE.get_height()))
      self.screen.blit(ANGRY_BEAR_IMAGE, (self.bear_x, self.bear_y))
    else:
      self.screen.blit(BEAR_IMAGE, (self.bear_x, self.bear_y))

  def create_bees(self, number_of_bees):
    for _ in range(number_of_bees):
      random_x = random.randint(400, 1000) 
      random_y = random.randint(300, 800) 
      bee = Bee(random_x, random_y)
      self.bees.append(bee)
  
  def update_bees_position(self):
    for bee in self.bees:
      bee.move()  # Update bee positions based on their movement logic

  def draw_bees(self):
    for bee in self.bees:
      if bee.movingRight:
        self.screen.blit(ENEMY_IMAGE, (bee.x, bee.y))
      else:
        self.screen.blit(FLIPPED_ENEMY_IMAGE, (bee.x, bee.y))

  def check_collisions(self):
    # Check collisions between bear and bees
    for bee_rect in self.bee_rects:
      if self.bear_rect.colliderect(bee_rect):
        # Collision actions here
        bee_index = self.bee_rects.index(bee_rect)
        del self.bees[bee_index]
        del self.bee_rects[bee_index]
        self.number_of_bees -= 1
        # decrease honey jar number
        self.number_of_honey_jars -= 1
        self.angry_timer = time.time()
        if (self.number_of_honey_jars <= 0):
          self.end_game("lost")

  def end_game(self, game_state):
    if game_state == "won":
      self.total_number_of_honey += self.number_of_honey_jars
      if self.total_number_of_honey >= 10:
        self.show_popup("Congratulations! You have completed the maze and you've collected enough honey for the winter!", ["Continue"], "complete")
      else:
        self.show_popup("Congratulations! You have completed the maze, but you still need to collect more honey!", ["Continue"], "ongoing")
    elif game_state == "lost":
      self.show_popup("Oh no! You lost all your honey! Collect some more and try again!", ["Continue"], "failed")
    self.maze_running = False
    
  def show_popup(self, message, buttons, state):
    popup_font = pygame.font.Font(None, FONT_SIZE)
    if state == "ongoing":
      font_colour = GRAY
      background_colour = WHITE
    elif state == "complete":
      font_colour = GOLD
      background_colour = BLACK
    else:
      font_colour = RED
      background_colour = WHITE
    popup_text = popup_font.render(message, True, font_colour)
    popup_rect = popup_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    popup_background = pygame.Surface((popup_rect.width + 20, popup_rect.height + 20))
    popup_background.fill(background_colour)
    popup_background_rect = popup_background.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        
    self.screen.blit(popup_background, popup_background_rect)
    self.screen.blit(popup_text, popup_rect)

    button_font = pygame.font.Font(None, FONT_SIZE)
    button_width, button_height = 120, 35
    button_x = (SCREEN_WIDTH - button_width) // 2
    button_y = popup_rect.bottom + 20

    for button_text in buttons:
      button_surface = button_font.render(button_text, True, font_colour)
      button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
      pygame.draw.rect(self.screen, background_colour, button_rect)
      self.screen.blit(button_surface, button_rect.topleft)
      button_x += button_width + 20

    pygame.display.flip()

    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
          mouse_pos = pygame.mouse.get_pos()
          if button_rect.collidepoint(mouse_pos):
            return

  def check_position(self, level):
    # R, L, U, D
    turns = [False, False, False, False]
    if self.goal_tile[0].collidepoint(self.center_x, self.center_y):
      self.end_game("won")
    if self.center_x // TILE_WIDTH < 30 and self.center_x // TILE_WIDTH > 1:
      # If you're currently moving RIGHT, you should be able to move LEFT, back to your initial position
      if self.direction == RIGHT:
        if level[self.center_y // TILE_HEIGHT][(self.center_x - TILE_WIDTH) // TILE_WIDTH] not in OBSTACLE:
          turns[1] = True
      # If you're currently moving LEFT, you should be able to move RIGHT, back to your initial position
      if self.direction == LEFT:
        if level[self.center_y // TILE_HEIGHT][(self.center_x + TILE_WIDTH) // TILE_WIDTH] not in OBSTACLE:
          turns[0] = True
      # If you're currently moving UP, you should be able to move DOWN, back to your initial position
      if self.direction == UP:
        if level[(self.center_y + TILE_HEIGHT) // TILE_HEIGHT][self.center_x // TILE_WIDTH] not in OBSTACLE:
          turns[3] = True
      # If you're currently moving DOWN, you should be able to move UP, back to your initial position
      if self.direction == DOWN:
        if level[(self.center_y - TILE_HEIGHT) // TILE_HEIGHT][self.center_x // TILE_WIDTH] not in OBSTACLE:
          turns[2] = True

      if self.direction == UP or self.direction == DOWN:
        if level[(self.center_y + C9_FUDGE_FACTOR) // TILE_HEIGHT][self.center_x // TILE_WIDTH] not in OBSTACLE:
          turns[3] = True
        if level[(self.center_y - C9_FUDGE_FACTOR) // TILE_HEIGHT][self.center_x // TILE_WIDTH] not in OBSTACLE:
          turns[2] = True
        if level[self.center_y // TILE_HEIGHT][(self.center_x - TILE_WIDTH) // TILE_WIDTH] not in OBSTACLE:
          turns[1] = True
        if level[self.center_y // TILE_HEIGHT][(self.center_x + TILE_WIDTH) // TILE_WIDTH] not in OBSTACLE:
          turns[0] = True

      if self.direction == RIGHT or self.direction == LEFT:
        if level[(self.center_y + TILE_HEIGHT) // TILE_HEIGHT][self.center_x // TILE_WIDTH] not in OBSTACLE:
          turns[3] = True
        if level[(self.center_y - TILE_HEIGHT) // TILE_HEIGHT][self.center_x // TILE_WIDTH] not in OBSTACLE:
          turns[2] = True
        if level[self.center_y // TILE_HEIGHT][(self.center_x - C9_FUDGE_FACTOR) // TILE_WIDTH] not in OBSTACLE:
          turns[1] = True
        if level[self.center_y // TILE_HEIGHT][(self.center_x + C9_FUDGE_FACTOR) // TILE_WIDTH] not in OBSTACLE:
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

  def draw_counters(self):
    jar_msg = f"Number of Jars: {self.number_of_honey_jars}"
    bee_msg = f"Number of Bees: {self.number_of_bees}"
    
    font = pygame.font.Font(None, FONT_SIZE)
    
    jar_surface = font.render(jar_msg, True, (0, 0, 0))
    bee_surface = font.render(bee_msg, True, (0, 0, 0))
    
    jar_background_rect  = pygame.draw.rect(self.screen, COLOR, pygame.Rect((5 * TILE_WIDTH, 6 * TILE_HEIGHT, 3.7 * TILE_WIDTH, TILE_HEIGHT)))
    bee_background_rect  = pygame.draw.rect(self.screen, COLOR, pygame.Rect((21.3 * TILE_WIDTH, 6 * TILE_HEIGHT, 3.7 * TILE_WIDTH, TILE_HEIGHT)))
    
    self.screen.blit(jar_surface, (jar_background_rect.x + 10, jar_background_rect.y + 5))
    self.screen.blit(bee_surface, (bee_background_rect.x + 10, bee_background_rect.y + 5))
        
  def draw_help_button(self):
    margin = 5  # Space between the bottom of the counter and the top of the help button
    # Calculate the x-coordinate based on the counter's position and potentially its width if needed
    help_button_x = 5 * TILE_WIDTH
    # Assuming the counter's height is TILE_HEIGHT, calculate the y-coordinate to place the button below it
    help_button_y = (6 * TILE_HEIGHT + TILE_HEIGHT) + margin  # Just below the "Number of Bees" rectangle

    self.screen.blit(HELP_IMAGE, (help_button_x, help_button_y))
    self.help_button_rect = HELP_IMAGE.get_rect(topleft=(help_button_x, help_button_y))

  def draw_tutorial(self):
    tutorial_x = (SCREEN_WIDTH - TUTORIAL_IMAGE.get_width()) // 2
    tutorial_y = (SCREEN_HEIGHT - TUTORIAL_IMAGE.get_height()) // 2
    self.screen.blit(TUTORIAL_IMAGE, (tutorial_x, tutorial_y))
  
  
  def run(self):
    while self.maze_running:
      direction = None
      self.timer.tick(FPS)
      self.screen.fill(COLOR)
      self.draw_maze(LEVEL)
      self.draw_counters()
      self.draw_bear()
      self.update_bees_position()
      self.draw_bees()
      self.draw_help_button()
      
      
      # Update bear and bee Rect objects
      self.bear_rect.update(self.bear_x, self.bear_y, BEAR_IMAGE.get_width(), BEAR_IMAGE.get_height())
      self.bee_rects = [pygame.Rect(bee.x, bee.y, ENEMY_IMAGE.get_width(), ENEMY_IMAGE.get_height()) for bee in self.bees]

      # Check collisions
      self.check_collisions()

      self.center_x = self.bear_x + CENTER_ADJUSTMENT
      self.center_y = self.bear_y + CENTER_ADJUSTMENT
      turns_allowed = self.check_position(LEVEL)
      for event in pygame.event.get():
        if event.type == pygame.QUIT: 
          quit()

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
        if self.help_button_rect.collidepoint(position):
          self.draw_tutorial()


      for i in range(len(turns_allowed)):
        if direction == i and turns_allowed[i]:
          self.direction = i
          self.bear_x, self.bear_y = self.move_bear(self.bear_x, self.bear_y, turns_allowed)

      pygame.display.flip()
