import pygame
from pygame.locals import *


class Ball:

    MaxVELOCITY = 50

    def __init__(self, xVelocity):

        #  Set basic variables for ball
        self.surface = pygame.display.get_surface()
        self.x = 635
        self.y = 360
        self.RADIUS = 15
        self.xVelocity = xVelocity
        self.yVelocity = 0
        self.startBallFlag = False

        pygame.draw.circle(self.surface, (255, 255, 255), (self.x, self.y), self.RADIUS, 0)
        
    
    def moveBall(self):
        self.x += self.xVelocity
        self.y += self.yVelocity        
    
    def startBall(self):
        if not self.startBallFlag:        
            self.moveBall()
            self.startBallFlag = True
            
    def drawBall(self):
        pygame.draw.circle(self.surface, (255, 255, 255), (self.x, self.y), self.RADIUS, 0)