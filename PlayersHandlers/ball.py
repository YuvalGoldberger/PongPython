import random
import pygame
from pygame.locals import *
from config import Config


class Ball:

    MaxVELOCITY = 50

    def __init__(self):
        '''
        Initiate Ball and set default values.
        '''

        #  Set basic variables for ball
        self.x = 635
        self.y = 360
        self.RADIUS = 15
        self.yVelocity = 0
        self.xVelocity = random.choice([Config().BALL_SPEED, -1 * Config().BALL_SPEED])
        self.startBallFlag = False

    def moveBall(self):
        '''
        Changes Ball x,y values using the Velocity.
        '''
        self.x += self.xVelocity
        self.y += self.yVelocity     
    
    def startBall(self):
        '''
        Starts the ball movement. Being called when pressed "Enter" on game start or after score.
        '''
        if not self.startBallFlag:        
            self.moveBall()
            
            
    def drawBall(self, move):
        '''
        Displays the Ball.
        '''
        surface = pygame.display.get_surface()
        if int(move.split(':')[0])==0:
            self.x=float(move.split(':')[1])
            self.y=float(move.split(':')[2])
        pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), self.RADIUS, 0)

    
    def displayBasic(self):
        '''
        Displays Ball at its default values.
        '''
        surface = pygame.display.get_surface()
        self.x = 635
        self.y = 360
        pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), self.RADIUS, 0)