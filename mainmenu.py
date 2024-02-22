import pygame
import sys

pygame.init()

screenWidth,screenHeight = 1920,1080
screen = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption("Main Menu")

# Temporary background color,will change soon...
backgroundColor = (181,101,29)
textColor = (255,255,255)
buttonBackgroundColor = (0,0,0)
buttonWidth = 200
buttonHeight= 50


gradelevel = 4


# Temporary font,will be changed when the font is selected for our project
font = pygame.font.Font(None,36)

#Change the logo path later when folder structure is created
logo = pygame.image.load('logo.png')
logoRect = logo.get_rect(center=(screenWidth//2,450))


buttonPlay = pygame.Rect(screenWidth//2 - 100,850,buttonWidth,buttonHeight)
buttonFourth = pygame.Rect(screenWidth // 2 - buttonWidth -50,600,buttonWidth,buttonHeight)  
buttonFifth = pygame.Rect(screenWidth // 2 + 50,600,buttonWidth,buttonHeight)    

showPlayButton = True
showLogo = True

#Used so that text is displayed centered
def drawText(text, font, color, rect):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)



running = True
while running:
    screen.fill(backgroundColor)
    
    if showLogo:
        screen.blit(logo,logoRect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if showPlayButton and buttonPlay.collidepoint(event.pos):
                showPlayButton = False
                showLogo = False 
            elif buttonFourth.collidepoint(event.pos):
                gradeLevel = 4
            elif buttonFifth.collidepoint(event.pos):
                gradeLevel = 5

    if showPlayButton:
        pygame.draw.rect(screen,buttonBackgroundColor,buttonPlay)
        drawText('Play',font,textColor,buttonPlay)
    else:
        gradeSelectText = font.render('Select your grade',True,textColor)
        screen.blit(gradeSelectText,(screenWidth // 2 - 100,550))

        pygame.draw.rect(screen,buttonBackgroundColor,buttonFourth)
        drawText('Fourth',font,textColor,buttonFourth)
        
        pygame.draw.rect(screen,buttonBackgroundColor,buttonFifth)
        drawText('Fifth',font,textColor,buttonFifth)
        

    pygame.display.flip()
