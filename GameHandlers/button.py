import pygame
from pygame.locals import *

class Button:
    def __init__(self, imgLoc, x, y):
        self.x = x
        self.y = y
        #Pre-Selected by me
        self.imgWidth = 200
        self.imgHeight = 60
        self.imgLocation = imgLoc
        self.surface = pygame.display.get_surface()
        self.screenHeight = self.surface.get_height()
        self.screenWidth = self.surface.get_width()


        img = pygame.image.load(self.imgLocation).convert_alpha()
        self.surface.blit(img, (self.x, self.y))

    def displayButton(self):
        img = pygame.image.load(self.imgLocation).convert_alpha()
        self.surface.blit(img, (self.x, self.y))

    def checkPressed(self, cursorX, cursorY):
        if(cursorX >= self.x and cursorX <= self.x + self.imgWidth) and (cursorY >= self.y and cursorY <= self.y + self.imgHeight):
            return True
        else:
            return False

    def displayState(self, state):
        font = pygame.font.Font(r'D:\Yuval_Python\Yuval Final Proj\Game\Fonts\Assistant-ExtraBold.ttf', 35)
        stateText = font.render(state, 1, (50, 255, 20))

        if state == "AI":
            pygame.display.get_surface().blit(stateText, ((self.screenWidth / 2) - 10, self.screenHeight - 60))
        elif state == "MultiPlayer":      
            pygame.display.get_surface().blit(stateText, ((self.screenWidth / 2) - 80, self.screenHeight - 60))
        elif state == "Impossible":      
            pygame.display.get_surface().blit(stateText, ((self.screenWidth / 2) - 75, self.screenHeight - 60))