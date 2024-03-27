import pygame
import sys


# To whoever is combining the app together:
# Just skip to lines 157 annd 163. 
# Those buttons correspond to the grade level options, which will then begin the game.
#
#

pygame.init()

screenWidth, screen_height = 1280, 720
screen = pygame.display.set_mode((screenWidth, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Unbearable Spelling Bees!")

#Image Section
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (screenWidth, screen_height))
logo = pygame.image.load("logo.png")
start_button_normal = pygame.image.load("Buttons/playbutton.png").convert_alpha()
start_button_hover = pygame.image.load("Buttons/playbutton_sel.png").convert_alpha()
quit_button_normal = pygame.image.load("Buttons/quitbutton.png").convert_alpha()
quit_button_hover = pygame.image.load("Buttons/quitbutton_sel.png").convert_alpha()
easy_button_normal = pygame.image.load("Buttons/easybutton.png").convert_alpha()
easy_button_hover = pygame.image.load("Buttons/easybutton_sel.png").convert_alpha()
hard_button_normal = pygame.image.load("Buttons/hardbutton.png").convert_alpha()
hard_button_hover = pygame.image.load("Buttons/hardbutton_sel.png").convert_alpha()
back_button_normal = pygame.image.load("Buttons/backbutton.png").convert_alpha()
back_button_hover = pygame.image.load("Buttons/backbutton_sel.png").convert_alpha()
tutorial_button_normal = pygame.image.load("Buttons/tutorialbutton.png").convert_alpha()
tutorial_button_hover = pygame.image.load("Buttons/tutorialbutton_sel.png").convert_alpha()

#Font Section
font_path = "Fonts/Honey.ttf"
font = pygame.font.Font(font_path, 40)
titleFont = pygame.font.Font(font_path, 80)

backgroundColor = (255, 227, 159)

MENU = 1
DIFFICULTY_SELECTION = 2
state = MENU

# This function allows the logo to scale dynamicaly depend on screensize (Button size not done, can crash when the user tries to drag the window too small)
def scale_and_position_elements(screenWidth, screen_height):
    
    logo_width, logo_height = 1145, 686
    scale_factor = min((screenWidth - 100) / logo_width, (screen_height - 200) / logo_height)
    scaled_logo = pygame.transform.scale(logo, (int(logo_width * scale_factor), int(logo_height * scale_factor))) if scale_factor < 1 else logo

    logo_x = (screenWidth - scaled_logo.get_width())// 2
    logo_y = (screen_height - scaled_logo.get_height()- 100 - button_height * 2) // 2
    start_button_x = (screenWidth - button_width)//2
    start_button_y = logo_y + scaled_logo.get_height()+20
    
    

    quit_button_x = (screenWidth - button_width)//2
    quit_button_y = start_button_y + button_height+10

    #Not yet implemmented 
    tutorial_button_x = (screenWidth - button_width)//2
    tutorial_button_y = start_button_y + button_height+10
    
    easy_button_x = screenWidth //2 - 250 
    easy_button_y = screen_height //2
    hard_button_x = screenWidth //2 + 50 
    hard_button_y = screen_height //2

    back_button_x = screenWidth // 2 - button_width // 2
    back_button_y = screen_height -button_height- 20  
    
    return scaled_logo, logo_x, logo_y, start_button_x, start_button_y, quit_button_x, quit_button_y, easy_button_x, easy_button_y, hard_button_x, hard_button_y, back_button_x, back_button_y


button_width, button_height = 200, 50

scaled_logo, logo_x, logo_y, start_button_x, start_button_y, quit_button_x, quit_button_y, easy_button_x, easy_button_y, hard_button_x, hard_button_y,back_button_x, back_button_y = scale_and_position_elements(screenWidth, screen_height)

def check_button_hover(button_x, button_y, mouse_x, mouse_y):
    if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height:
        return True
    return False

def draw_menu():
    screen.blit(background, (0, 0))
    screen.blit(scaled_logo, (logo_x, logo_y))

    mouse_x, mouse_y = pygame.mouse.get_pos()
    if check_button_hover(start_button_x, start_button_y, mouse_x, mouse_y):
        screen.blit(start_button_hover, (start_button_x, start_button_y))
    else:
        screen.blit(start_button_normal, (start_button_x, start_button_y))

    if check_button_hover(quit_button_x, quit_button_y, mouse_x, mouse_y):
        screen.blit(quit_button_hover, (quit_button_x, quit_button_y))
    else:
        screen.blit(quit_button_normal, (quit_button_x, quit_button_y))

def draw_difficulty_selection():
    screen.fill(backgroundColor)
    
    title_surf = titleFont.render("SELECT DIFFICULTY", True, (0, 0, 0))
    title_rect = title_surf.get_rect(center=(screenWidth // 2, 100))
    screen.blit(title_surf, title_rect)
    
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Easy button
    easy_button_rect = easy_button_normal.get_rect(center=(easy_button_x + button_width // 2, easy_button_y + button_height // 2))
    if easy_button_rect.collidepoint(mouse_x, mouse_y):
        screen.blit(easy_button_hover, easy_button_rect.topleft)
        easy_text_surf = font.render("EASY: INTENDED FOR STUDENTS GRADE 4 AND BELOW", True, (0, 0, 0))
        easy_text_rect = easy_text_surf.get_rect(center=(easy_button_x + button_width // 2, easy_button_y + button_height + 50))
        screen.blit(easy_text_surf, easy_text_rect.topleft)
    else:
        screen.blit(easy_button_normal, easy_button_rect.topleft)
    
    # Hard button
    hard_button_rect = hard_button_normal.get_rect(center=(hard_button_x + button_width // 2, hard_button_y + button_height // 2))
    if hard_button_rect.collidepoint(mouse_x, mouse_y):
        screen.blit(hard_button_hover, hard_button_rect.topleft)
        hard_text_surf = font.render("HARD: INTENDED FOR STUDENTS GRADE 5 AND ABOVE", True, (0, 0, 0))
        hard_text_rect = hard_text_surf.get_rect(center=(hard_button_x + button_width // 2, hard_button_y + button_height + 50))
        screen.blit(hard_text_surf, hard_text_rect.topleft)
    else:
        screen.blit(hard_button_normal, hard_button_rect.topleft)
    # Back 
    back_button_rect = back_button_normal.get_rect(center=(back_button_x + button_width // 2, back_button_y + button_height // 2))
    if back_button_rect.collidepoint(mouse_x, mouse_y):
        screen.blit(back_button_hover, back_button_rect.topleft)
    else:
        screen.blit(back_button_normal, back_button_rect.topleft)




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
                back_button_rect = back_button_normal.get_rect(center=(back_button_x + button_width // 2, back_button_y + button_height // 2))
                if back_button_rect.collidepoint(mouse_x, mouse_y):
                    state = MENU
                elif check_button_hover(easy_button_x, easy_button_y, mouse_x, mouse_y):
                    print("Easy difficulty selected")
                    #Grade 4 Option 


                    
                elif check_button_hover(hard_button_x, hard_button_y, mouse_x, mouse_y):
                    print("Hard difficulty selected")
                    #Grade 5 Option





                    
        elif event.type == pygame.VIDEORESIZE:
            screenWidth, screen_height = event.size
            screen = pygame.display.set_mode((screenWidth, screen_height), pygame.RESIZABLE)
            background = pygame.transform.scale(background, (screenWidth, screen_height))
            scaled_logo, logo_x, logo_y, start_button_x, start_button_y, quit_button_x, quit_button_y, easy_button_x, easy_button_y, hard_button_x, hard_button_y, back_button_x, back_button_y = scale_and_position_elements(screenWidth, screen_height)

    if state == MENU:
        draw_menu()
    elif state == DIFFICULTY_SELECTION:
        draw_difficulty_selection()

    pygame.display.flip()

pygame.quit()


