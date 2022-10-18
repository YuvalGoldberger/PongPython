import pygame
from pygame.locals import *
import random

class Player:
    
    def __init__(self, x):

        self.surface = pygame.display.get_surface()
        HEIGHT = self.surface.get_height()
        self.y = HEIGHT / 2 - 85
        self.x = x
        self.playerHeight = 170
        self.playerWidth = 40
        
        self.playerColors = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        pygame.draw.rect(self.surface, self.playerColors , (self.x, self.y, self.playerWidth, self.playerHeight))
        
    def movePlayer(self, state):
        if state == "UP":
            self.y -= 8
            #  Check if Player collides with screen Y limit
            if self.y <= 0:
                self.y += 30
            
        if state == "DOWN":
            self.y += 8
            #  Check if Player collides with screen Y limit
            if self.y >= pygame.display.get_surface().get_height() - 170:
                self.y -= 30
           
        pygame.display.flip()
        return self.y

    def drawPlayer(self):
        pygame.draw.rect(self.surface, self.playerColors , (self.x, self.y, self.playerWidth, self.playerHeight))
