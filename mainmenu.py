import pygame
import sys
from bear_maze.game import BearMazeGame

pygame.init()

screenWidth, screen_height = 1920,1080
screen = pygame.display.set_mode((screenWidth, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Unbearable Spelling Bees!")

#Image Section
BACKGROUND = pygame.transform.scale(pygame.image.load("background.jpg"), (screenWidth, screen_height))
LOGO = pygame.image.load("logo.png")
START_BUTTON_NORMAL = pygame.image.load("Buttons/playbutton.png").convert_alpha()
START_BUTTON_HOVER = pygame.image.load("Buttons/playbutton_sel.png").convert_alpha()
QUIT_BUTTON_NORMAL = pygame.image.load("Buttons/quitbutton.png").convert_alpha()
QUIT_BUTTON_HOVER = pygame.image.load("Buttons/quitbutton_sel.png").convert_alpha()
EASY_BUTTON_NORMAL = pygame.image.load("Buttons/easybutton.png").convert_alpha()
EASY_BUTTON_HOVER = pygame.image.load("Buttons/easybutton_sel.png").convert_alpha()
HARD_BUTTON_NORMAL = pygame.image.load("Buttons/hardbutton.png").convert_alpha()
HARD_BUTTON_HOVER = pygame.image.load("Buttons/hardbutton_sel.png").convert_alpha()
BACK_BUTTON_NORMAL = pygame.image.load("Buttons/backbutton.png").convert_alpha()
BACK_BUTTON_HOVER = pygame.image.load("Buttons/backbutton_sel.png").convert_alpha()
TUTORIAL_BUTTON_NORMAL = pygame.image.load("Buttons/tutorialbutton.png").convert_alpha()
TUTORIAL_BUTTON_HOVER = pygame.image.load("Buttons/tutorialbutton_sel.png").convert_alpha()
STARTING_NUMBER_OF_BEES = 3
STARTING_NUMBER_OF_HONEY_JARS = 3
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50

#Font Section
font_path = "Fonts/Honey.ttf"
font = pygame.font.Font(font_path, 40)
titleFont = pygame.font.Font(font_path, 80)

backgroundColor = (255, 227, 159)

MENU = 1
DIFFICULTY_SELECTION = 2
state = MENU

# This function allows the logo to scale dynamically depend on screensize (Button size not done, can crash when the user tries to drag the window too small)
def scale_and_position_elements(screenWidth, screen_height):
  logo_width, logo_height = 1145, 686
  scale_factor = min((screenWidth - 100) / logo_width, (screen_height - 200) / logo_height)
  scaled_logo = pygame.transform.scale(LOGO, (int(logo_width * scale_factor), int(logo_height * scale_factor))) if scale_factor < 1 else LOGO

  logo_x = (screenWidth - scaled_logo.get_width())// 2
  logo_y = (screen_height - scaled_logo.get_height()- 100 - BUTTON_HEIGHT * 2) // 2
  start_button_x = (screenWidth - BUTTON_WIDTH)//2
  start_button_y = logo_y + scaled_logo.get_height()

  quit_button_x = (screenWidth - BUTTON_WIDTH)//2
  quit_button_y = start_button_y + BUTTON_HEIGHT+10

  # Not yet implemented 
  tutorial_button_x = (screenWidth - BUTTON_WIDTH)//2
  tutorial_button_y = start_button_y + BUTTON_HEIGHT+10
  
  easy_button_x = screenWidth //2 - 250 
  easy_button_y = screen_height //2
  hard_button_x = screenWidth //2 + 50 
  hard_button_y = screen_height //2

  back_button_x = screenWidth // 2 - BUTTON_WIDTH // 2
  back_button_y = screen_height -BUTTON_HEIGHT- 250  
  
  return scaled_logo, logo_x, logo_y, start_button_x, start_button_y, quit_button_x, quit_button_y, easy_button_x, easy_button_y, hard_button_x, hard_button_y, back_button_x, back_button_y

scaled_logo, logo_x, logo_y, start_button_x, start_button_y, quit_button_x, quit_button_y, easy_button_x, easy_button_y, hard_button_x, hard_button_y,back_button_x, back_button_y = scale_and_position_elements(screenWidth, screen_height)

def check_button_hover(button_x, button_y, mouse_x, mouse_y):
  if button_x < mouse_x < button_x + BUTTON_WIDTH and button_y < mouse_y < button_y + BUTTON_HEIGHT:
    return True
  return False

def draw_menu():
  screen.blit(BACKGROUND, (0, 0))
  screen.blit(scaled_logo, (logo_x, logo_y))

  mouse_x, mouse_y = pygame.mouse.get_pos()
  if check_button_hover(start_button_x, start_button_y, mouse_x, mouse_y):
    screen.blit(START_BUTTON_HOVER, (start_button_x, start_button_y))
  else:
    screen.blit(START_BUTTON_NORMAL, (start_button_x, start_button_y))

  if check_button_hover(quit_button_x, quit_button_y, mouse_x, mouse_y):
    screen.blit(QUIT_BUTTON_HOVER, (quit_button_x, quit_button_y))
  else:
    screen.blit(QUIT_BUTTON_NORMAL, (quit_button_x, quit_button_y))

def draw_difficulty_selection():
  screen.fill(backgroundColor)
  
  title_surf = titleFont.render("SELECT DIFFICULTY", True, (0, 0, 0))
  title_rect = title_surf.get_rect(center=(screenWidth // 2, 100))
  screen.blit(title_surf, title_rect)
  
  mouse_x, mouse_y = pygame.mouse.get_pos()
  
  # Easy button
  easy_button_rect = EASY_BUTTON_NORMAL.get_rect(center=(easy_button_x + BUTTON_WIDTH // 2, easy_button_y + BUTTON_HEIGHT // 2))
  if easy_button_rect.collidepoint(mouse_x, mouse_y):
    screen.blit(EASY_BUTTON_HOVER, easy_button_rect.topleft)
    easy_text_surf = font.render("EASY: INTENDED FOR STUDENTS GRADE 4 AND BELOW", True, (0, 0, 0))
    easy_text_rect = easy_text_surf.get_rect(center=(easy_button_x + BUTTON_WIDTH // 2, easy_button_y + BUTTON_HEIGHT + 50))
    screen.blit(easy_text_surf, easy_text_rect.topleft)
  else:
    screen.blit(EASY_BUTTON_NORMAL, easy_button_rect.topleft)
  
  # Hard button
  hard_button_rect = HARD_BUTTON_NORMAL.get_rect(center=(hard_button_x + BUTTON_WIDTH // 2, hard_button_y + BUTTON_HEIGHT // 2))
  if hard_button_rect.collidepoint(mouse_x, mouse_y):
    screen.blit(HARD_BUTTON_HOVER, hard_button_rect.topleft)
    hard_text_surf = font.render("HARD: INTENDED FOR STUDENTS GRADE 5 AND ABOVE", True, (0, 0, 0))
    hard_text_rect = hard_text_surf.get_rect(center=(hard_button_x + BUTTON_WIDTH // 2, hard_button_y + BUTTON_HEIGHT + 50))
    screen.blit(hard_text_surf, hard_text_rect.topleft)
  else:
    screen.blit(HARD_BUTTON_NORMAL, hard_button_rect.topleft)

  # Back 
  back_button_rect = BACK_BUTTON_NORMAL.get_rect(center=(back_button_x + BUTTON_WIDTH // 2, back_button_y + BUTTON_HEIGHT // 2))
  if back_button_rect.collidepoint(mouse_x, mouse_y):
    screen.blit(BACK_BUTTON_HOVER, back_button_rect.topleft)
  else:
    screen.blit(BACK_BUTTON_NORMAL, back_button_rect.topleft)

def start_game(): 
  game = BearMazeGame(STARTING_NUMBER_OF_BEES, STARTING_NUMBER_OF_HONEY_JARS)
  game.run()

running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
      mouse_x, mouse_y = pygame.mouse.get_pos()
      if state == MENU:
        if check_button_hover(start_button_x, start_button_y, mouse_x, mouse_y):
          state = DIFFICULTY_SELECTION 
        elif check_button_hover(quit_button_x, quit_button_y, mouse_x, mouse_y):
          running = False
      elif state == DIFFICULTY_SELECTION:
        back_button_rect = BACK_BUTTON_NORMAL.get_rect(center=(back_button_x + BUTTON_WIDTH // 2, back_button_y + BUTTON_HEIGHT // 2))
        if back_button_rect.collidepoint(mouse_x, mouse_y):
          state = MENU
        elif check_button_hover(easy_button_x, easy_button_y, mouse_x, mouse_y):
          start_game()
        elif check_button_hover(hard_button_x, hard_button_y, mouse_x, mouse_y):
          start_game()
    elif event.type == pygame.VIDEORESIZE:
      screenWidth, screen_height = event.size
      screen = pygame.display.set_mode((screenWidth, screen_height), pygame.RESIZABLE)
      BACKGROUND = pygame.transform.scale(BACKGROUND, (screenWidth, screen_height))
      scaled_logo, logo_x, logo_y, start_button_x, start_button_y, quit_button_x, quit_button_y, easy_button_x, easy_button_y, hard_button_x, hard_button_y, back_button_x, back_button_y = scale_and_position_elements(screenWidth, screen_height)

  if state == MENU:
    draw_menu()
  elif state == DIFFICULTY_SELECTION:
    draw_difficulty_selection()

  pygame.display.flip()

pygame.quit()
