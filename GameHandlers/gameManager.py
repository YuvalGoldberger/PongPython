import pygame
from pygame.locals import *
import random

from PlayersHandlers.player import Player
from PlayersHandlers.ball import Ball

from GameHandlers.impossible import Impossible

class GameManager:
    pygame.font.init()

    def __init__(self):
        self.firstPlayer = Player(30)
        self.secondPlayer = Player(1210)
        self.ball = Ball(random.choice((-7, 7)))
        self.impossiblePlayer = Impossible(self.secondPlayer, self.ball)
        self.screenHeight = pygame.display.get_surface().get_height()
        self.screenWidth = pygame.display.get_surface().get_width()
        self.firstPlayerPoints = 0
        self.secondPlayerPoints = 0

        self.canSelect = True
        
        
    def checkCollision(self):
        playerHeight = 170
        playerWidth = 40

        #  Screen Limit (y) Colission
        if self.ball.y + self.ball.RADIUS >= self.screenHeight:
            self.ball.yVelocity *= -1
            self.ball.y -= 5

        elif self.ball.y - self.ball.RADIUS <= 0:
            self.ball.yVelocity *= -1
            self.ball.y += 5

        #  Ball Collision
        if ((self.ball.x - self.ball.RADIUS <= self.firstPlayer.x + playerWidth) and (self.ball.x - self.ball.RADIUS >= self.firstPlayer.x)) and \
             (self.ball.y >= self.firstPlayer.y and self.ball.y <= self.firstPlayer.y + playerHeight):
            if self.ball.xVelocity < self.ball.MaxVELOCITY:
                self.ball.xVelocity -= 0.2
            self.ball.xVelocity *= -1
            self.ball.x += 10

            #  Choose yVelocity of the ball after colission, depends on hit location (above middle will go up, beneath middle will go down)
            midY = self.firstPlayer.y + playerHeight / 2
            subY = midY - self.ball.y
            reductionFactor = (playerHeight / 2) / self.ball.xVelocity
            self.ball.yVelocity = -1 * subY / reductionFactor


        if ((self.ball.x + self.ball.RADIUS >= self.secondPlayer.x) and (self.ball.x + self.ball.RADIUS <= self.secondPlayer.x + playerWidth)) and \
            (self.ball.y >= self.secondPlayer.y and self.ball.y <= self.secondPlayer.y + playerHeight):
            if self.ball.xVelocity < -1 * self.ball.MaxVELOCITY:
                self.ball.xVelocity += 0.2
            self.ball.xVelocity *= -1
            self.ball.x -= 10

            #  Choose yVelocity of the ball after colission, depends on hit location (above middle will go up, beneath middle will go down)
            midY = self.secondPlayer.y + playerHeight / 2
            subY = midY - self.ball.y
            reductionFactor = (playerHeight / 2) / self.ball.xVelocity
            self.ball.yVelocity = -1 * subY / reductionFactor

        #  Goal (x Colission)
        if self.ball.x + self.ball.RADIUS >= self.screenWidth:
            self.ball.__init__(7)
            self.firstPlayer.__init__(self.firstPlayer.x)
            self.secondPlayer.__init__(self.secondPlayer.x)
            self.firstPlayerPoints += 1
            self.canSelect = True
        if self.ball.x + self.ball.RADIUS <= 0:
            self.ball.__init__(-7)
            self.firstPlayer.__init__(self.firstPlayer.x)
            self.secondPlayer.__init__(self.secondPlayer.x)
            self.secondPlayerPoints += 1
            self.canSelect = True
    
    def madeByDisplay(self):
        font = pygame.font.Font(r'D:\Yuval_Python\Yuval Final Proj\Game\Fonts\Assistant-ExtraBold.ttf', 35)
        madeByText = font.render("This game has been created by Yuval Goldberger!", 1, (50, 255, 20))
        pygame.display.get_surface().blit(madeByText, ((self.screenWidth / 2) - 380, 20))

    def scoreDisplay(self):
        scoreFont = pygame.font.Font(r'D:\Yuval_Python\Yuval Final Proj\Game\Fonts\Assistant-ExtraBold.ttf', 50)
        pointFont = pygame.font.Font(r'D:\Yuval_Python\Yuval Final Proj\Game\Fonts\Assistant-Medium.ttf', 30)
        scoreText = scoreFont.render("SCORE", 1, (255, 255, 255))
        firstPointsTtext = pointFont.render(str(self.firstPlayerPoints), 1, (255, 255, 255))
        secondPointsTtext = pointFont.render(str(self.secondPlayerPoints), 1, (255, 255, 255))

        pygame.display.get_surface().blit(scoreText, ((self.screenWidth / 2) - 75, 30 ))
        pygame.display.get_surface().blit(firstPointsTtext, ((self.screenWidth / 2) - 150, 90 ))
        pygame.display.get_surface().blit(secondPointsTtext, ((self.screenWidth / 2) + 150, 90 ))
    
    def startingGameAlert(self):

        font = pygame.font.Font(r'D:\Yuval_Python\Yuval Final Proj\Game\Fonts\Assistant-Bold.ttf', 30)
        pressEnterText = font.render("Press ENTER to start the game!", 1, (255, 255, 255))
        pygame.display.get_surface().blit(pressEnterText, ((self.screenWidth / 2) - 200, (self.screenHeight / 2) - 75 ))

    def resetScore(self):
        self.firstPlayerPoints = 0
        self.secondPlayerPoints = 0