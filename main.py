
import pygame
from pygame.locals import *
import random
import math

class GUI:

    def __init__(self):
        pygame.init()
        
        self.surface = pygame.display.set_mode((1270,720))
        pygame.display.set_caption("Yuval - Game Test")

        gameFlag = True
        madeByFlag = False
        
        clock = pygame.time.Clock()
    
        firstPlayer = Player(30)
        secondPlayer = Player(1210)
        ball = Ball(random.choice((-5, 5)))
        gameManager = Game(firstPlayer, secondPlayer, ball)

        
        pygame.display.flip()
        while gameFlag:
            clock.tick(60)
            for event in pygame.event.get():

                if event.type == QUIT:
                    gameFlag = False

            keys = pygame.key.get_pressed()

            if keys[K_RETURN]:
                ball.startBall()
                madeByFlag = True
            if keys[K_w]:
                firstPlayer.movePlayer("up")
            elif keys[K_s]:
                firstPlayer.movePlayer("down")
            if keys[K_UP]:
                secondPlayer.movePlayer("up")
            elif keys[K_DOWN]:
                secondPlayer.movePlayer("down")        

            self.surface.fill((0, 0, 0))

            #Check if game started, if not move the ball
            if ball.startBallFlag:
                ball.moveBall()
            #If game did not start, show "Press Enter to start"
            if not ball.startBallFlag:
                gameManager.startingGameAlert()
                #Only for the first time, show "Made By Yuval"
                if not madeByFlag:
                    gameManager.madeByAlert()
            #After first time, show score (and not "Made by Yuval")
            if madeByFlag:
                gameManager.scoreDisplay()
            gameManager.checkCollision()
            ball.drawBall()
            firstPlayer.drawPlayer()
            secondPlayer.drawPlayer()
            pygame.display.flip()


class Game:
    pygame.font.init()

    def __init__(self, firstPlayer, secondPlayer, ball):
        self.firstPlayer = firstPlayer
        self.secondPlayer = secondPlayer
        self.ball = ball
        self.screenHeight = pygame.display.get_surface().get_height()
        self.screenWidth = pygame.display.get_surface().get_width()
        self.firstPlayerPoints = 0
        self.secondPlayerPoints = 0
        
        
    def checkCollision(self):
        playerHeight = 170
        playerWidth = 40

        #Screen Limit (y) Colission
        if self.ball.y + self.ball.RADIUS >= self.screenHeight:
            self.ball.yVelocity *= -1

        elif self.ball.y - self.ball.RADIUS <= 0:
            self.ball.yVelocity *= -1

        #Ball Collision
        if ((self.ball.x - self.ball.RADIUS <= self.firstPlayer.x + playerWidth) and (self.ball.x - self.ball.RADIUS >= self.firstPlayer.x)) and \
             (self.ball.y >= self.firstPlayer.y and self.ball.y <= self.firstPlayer.y + playerHeight):
            if self.ball.xVelocity > 30:
                self.ball.xVelocity += 3
            self.ball.xVelocity *= -1

            #Choose yVelocity of the ball after colission, depends on hit location (above middle will go up, beneath middle will go down)
            midY = self.firstPlayer.y + playerHeight / 2
            subY = midY - self.ball.y
            reductionFactor = (playerHeight / 2) / self.ball.xVelocity
            self.ball.yVelocity = -1 * subY / reductionFactor


        if ((self.ball.x + self.ball.RADIUS >= self.secondPlayer.x) and (self.ball.x + self.ball.RADIUS <= self.secondPlayer.x + playerWidth)) and \
            (self.ball.y >= self.secondPlayer.y and self.ball.y <= self.secondPlayer.y + playerHeight):
            if self.ball.xVelocity < -30:
                self.ball.xVelocity -= 3
            self.ball.xVelocity *= -1
            #Choose yVelocity of the ball after colission, depends on hit location (above middle will go up, beneath middle will go down)
            midY = self.secondPlayer.y + playerHeight / 2
            subY = midY - self.ball.y
            reductionFactor = (playerHeight / 2) / self.ball.xVelocity
            self.ball.yVelocity = -1 * subY / reductionFactor

        #Lose (x Colission)
        if self.ball.x + self.ball.RADIUS >= self.screenWidth:
            self.ball.__init__(5)
            self.firstPlayerPoints += 1
        if self.ball.x + self.ball.RADIUS <= 0:
            self.ball.__init__(-5)
            self.secondPlayerPoints += 1
    
    def madeByAlert(self):
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


class Player:
    
    def __init__(self, x):

        self.surface = pygame.display.get_surface()
        self.y = 60
        self.x = x
        self.playerColors = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        pygame.draw.rect(self.surface, self.playerColors , (self.x, self.y, 40, 170))
        
    def movePlayer(self, state):
        if state == "up":
            self.y -= 8
            #Check if Player collides with screen Y limit
            if self.y <= 0:
                self.y += 30
            
        if state == "down":
            self.y += 8
            #Check if Player collides with screen Y limit
            if self.y >= pygame.display.get_surface().get_height() - 170:
                self.y -= 30
           
        pygame.display.flip()
        return self.y

    def drawPlayer(self):
        pygame.draw.rect(self.surface, self.playerColors, (self.x, self.y, 40, 170))


class Ball:

    MaxVELOCITY = 30

    def __init__(self, xVelocity):

        #Set basic variables for ball
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

class Main:
    gui = GUI()

Main()