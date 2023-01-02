import pygame
from pygame.locals import *

from PlayersHandlers.ball import Ball

from config import Config

class GameManager:
    pygame.font.init()
    FOLDER_LOCATION = Config().FOLDER_LOCATION

    def __init__(self):
        '''
        Initiates default values and Ball.
        '''
        self.screenHeight = 720
        self.screenWidth = 1270
        self.leftPlayerPoints = 0
        self.rightPlayerPoints = 0  

        self.ball = Ball()
        
        
    def checkCollision(self, leftPlayerY, rightPlayerY):
        '''
        Method being in charge of checking ball's collision (being called from server.)
        '''
        playerHeight = 170
        playerWidth = 40
        rightPlayerX = 1210
        leftPlayerX = 80

        #  Screen Limit (y) Colission
        if self.ball.y + self.ball.RADIUS >= self.screenHeight:
            self.ball.yVelocity *= -1
            self.ball.y -= 5

        if self.ball.y - self.ball.RADIUS <= 0:
            self.ball.yVelocity *= -1
            self.ball.y += 5
        
        #  Ball Collision
        if ((self.ball.x - self.ball.RADIUS <= leftPlayerX + playerWidth) and (self.ball.x - self.ball.RADIUS >= leftPlayerX)) and \
            (self.ball.y >= leftPlayerY and self.ball.y <= leftPlayerY + playerHeight):
            if self.ball.xVelocity < self.ball.MaxVELOCITY:
                self.ball.xVelocity -= 0.2
            self.ball.xVelocity *= -1
            self.ball.x += 10

            #  Choose yVelocity of the ball after colission, depends on hit location (above middle will go up, beneath middle will go down)
            midY = leftPlayerY + playerHeight / 2
            subY = midY - self.ball.y
            reductionFactor = (playerHeight / 2) / self.ball.xVelocity
            self.ball.yVelocity = -1 * subY / reductionFactor


        if ((self.ball.x + self.ball.RADIUS >= rightPlayerX) and (self.ball.x + self.ball.RADIUS <= rightPlayerX + playerWidth)) and \
            (self.ball.y >= rightPlayerY and self.ball.y <= rightPlayerY + playerHeight):
            if self.ball.xVelocity < -1 * self.ball.MaxVELOCITY:
                self.ball.xVelocity += 0.2
            self.ball.xVelocity *= -1
            self.ball.x -= 10

            #  Choose yVelocity of the ball after colission, depends on hit location (above middle will go up, beneath middle will go down)
            midY = rightPlayerY + playerHeight / 2
            subY = midY - self.ball.y
            reductionFactor = (playerHeight / 2) / self.ball.xVelocity
            self.ball.yVelocity = -1 * subY / reductionFactor


        #  Goal (x Colission)
        if self.ball.x + self.ball.RADIUS >= self.screenWidth:
            self.ball.__init__()
            self.ball.xVelocity = Config().BALL_SPEED
            self.leftPlayerPoints += 1
            return f"SCORE:{self.leftPlayerPoints}:{self.rightPlayerPoints}---"

        if self.ball.x + self.ball.RADIUS <= 0:
            self.ball.__init__()
            self.ball.xVelocity = -1 * Config().BALL_SPEED
            self.rightPlayerPoints += 1   
            return f"SCORE:{self.leftPlayerPoints}:{self.rightPlayerPoints}---"
        
        return ""     
    