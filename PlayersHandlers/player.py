import pygame
from pygame.locals import *
import random

class Player:

    def __init__(self, rightPlayerColor, leftPlayerColor):
        '''
        Initiate BOTH players settings.
        '''

        self.surface = pygame.display.get_surface()
        self.HEIGHT = 720
        
        self.leftPlayerY = self.HEIGHT / 2 
        self.rightPlayerY = self.HEIGHT / 2

        self.playerHeight = 170
        self.playerWidth = 40

        self.rightPlayerColor = rightPlayerColor
        self.leftPlayerColor = leftPlayerColor

        
    def movePlayer(self, state, playerNum):
        '''
        Called when "KEYDOWN" pygame event triggers. Changes the player (depends on playerNum) y value. 
        '''
        if state == "UP":
            if playerNum == 1:
                self.leftPlayerY -=8
                #  Check if Player collides with screen Y limit
                if self.leftPlayerY <= 0:
                    self.leftPlayerY += 30
                return self.leftPlayerY

            elif playerNum == 2:
                #  Check if Player collides with screen Y limit
                self.rightPlayerY -= 8
                if self.rightPlayerY <= 0:
                    self.rightPlayerY += 30
                return self.rightPlayerY
            
        if state == "DOWN":
            if playerNum == 1:
                self.leftPlayerY +=8
                #  Check if Player collides with screen Y limit
                if self.leftPlayerY >= self.HEIGHT - self.playerHeight:
                    self.leftPlayerY -= 30
                return self.leftPlayerY

            elif playerNum == 2:
                #  Check if Player collides with screen Y limit
                self.rightPlayerY += 8
                if self.rightPlayerY >= self.HEIGHT - self.playerHeight:
                    self.rightPlayerY -= 30
                return self.rightPlayerY
            

    def drawPlayer(self,move):
        '''
        Displays the players on the screen.
        '''
            
        if int(move.split(':')[0])==1:
            self.leftPlayerY=float(move.split(':')[1])
        elif int(move.split(':')[0])==2:
            self.rightPlayerY=float(move.split(':')[1])

        pygame.draw.rect(self.surface, self.rightPlayerColor , (80, self.rightPlayerY, self.playerWidth, self.playerHeight))
        pygame.draw.rect(self.surface, self.leftPlayerColor , (1210, self.leftPlayerY, self.playerWidth, self.playerHeight))

    def displayBasic(self):
        '''
        Displays the players on the default place. (default y value)
        '''
        self.leftPlayerY = self.HEIGHT / 2 - 85
        self.rightPlayerY = self.HEIGHT / 2 - 85 
        pygame.draw.rect(self.surface, self.rightPlayerColor , (80, self.rightPlayerY, self.playerWidth, self.playerHeight))
        pygame.draw.rect(self.surface, self.leftPlayerColor , (1210, self.leftPlayerY, self.playerWidth, self.playerHeight))