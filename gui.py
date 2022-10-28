import pygame
from pygame.locals import *

from GameHandlers.button import Button
from GameHandlers.gameManager import GameManager


class GUI:
    WIDTH = 1270
    HEIGHT = 720

    def __init__(self):
        pygame.init()
        
        
        self.surface = pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        pygame.display.set_caption("Yuval - Pong Game")

        self.showStart()
        if self.sentName:
            self.showGame()


    def showStart(self):
        self.sentName = False
        self.name = ''
        uppercase = False
        boldFont = pygame.font.Font(r'D:\Yuval_Python\Yuval Final Proj\Game\Fonts\Assistant-ExtraBold.ttf', 35)
        mediumFont = pygame.font.Font(r'D:\Yuval_Python\Yuval Final Proj\Game\Fonts\Assistant-Medium.ttf', 20)
        
        sendNameButton = Button(r'D:\Yuval_Python\Yuval Final Proj\Game\Images\EnterName.png', self.WIDTH / 2 - 100, self.HEIGHT / 2 + 100)


        enterName = boldFont.render("Enter Name", 1, (255, 255, 255))
        nameText = mediumFont.render("...", 1, (255, 255, 255))

        sending = True
        while sending:
            
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    cursorX, cursorY = pygame.mouse.get_pos()
                    if sendNameButton.checkPressed(cursorX, cursorY):
                        self.sentName = True
                        sending = False
                        break
                elif event.type == KEYDOWN:
                    if event.key == K_DELETE or event.key == K_BACKSPACE:
                        self.name = self.name[0:len(self.name)-1]
                    elif event.key == K_CAPSLOCK:
                        uppercase = not uppercase
                    else:
                        if pygame.key.name(event.key) in 'abcdefghijklmnopqrstuvwxyz0123456789':
                            if uppercase:
                                self.name += pygame.key.name(event.key).upper()
                            else:
                                self.name += pygame.key.name(event.key)
            nameText = mediumFont.render(self.name, 1, (255, 255, 255))

            self.surface.fill((0, 0, 0))
            sendNameButton.displayButton()
            pygame.display.get_surface().blit(enterName, ((self.HEIGHT / 2) + 175, self.HEIGHT / 2 - 60))
            pygame.display.get_surface().blit(nameText, ((self.WIDTH / 2) - 50, self.HEIGHT / 2 ))
                     
            pygame.display.flip()
        


    def showGame(self):

        gameFlag = True
        self.madeByFlag = False
        #  Modes can be "Offline", "MultiPlayer", "Impossible"
        self.selectedMode = ""
        
        clock = pygame.time.Clock()
    
        self.gameManager = GameManager()
        self.firstPlayer = self.gameManager.firstPlayer
        self.secondPlayer = self.gameManager.secondPlayer
        self.ball = self.gameManager.ball
        impossiblePlayer = self.gameManager.impossiblePlayer

        self.buttonMultiPlayer = Button(r'D:\Yuval_Python\Yuval Final Proj\Game\Images\MultiPlayer.png',
                                     self.WIDTH / 2 + 100, self.HEIGHT / 2 + 100)
        self.buttonOffline = Button(r'D:\Yuval_Python\Yuval Final Proj\Game\Images\Offline.png', 
                            self.WIDTH / 2 - 100, self.HEIGHT / 2 + 200)
        self.buttonImpossible = Button(r'D:\Yuval_Python\Yuval Final Proj\Game\Images\Impossible.png', 
                            self.WIDTH / 2 - 300, self.HEIGHT / 2 + 100)
        
        pygame.display.flip()
        while gameFlag:
            clock.tick(120)
            for event in pygame.event.get():

                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    cursorX, cursorY = pygame.mouse.get_pos()
                    if self.gameManager.canSelect:
                        if self.buttonImpossible.checkPressed(cursorX, cursorY):
                            self.selectedMode = "Impossible"
                            self.gameManager.resetScore()
                        elif self.buttonMultiPlayer.checkPressed(cursorX, cursorY):
                            self.selectedMode = "MultiPlayer"
                            self.gameManager.resetScore()
                        elif self.buttonOffline.checkPressed(cursorX, cursorY):
                            self.selectedMode = "Offline" 
                            self.gameManager.resetScore()

                if event.type == QUIT:
                    gameFlag = False

            keys = pygame.key.get_pressed()

            if keys[K_RETURN]:
                self.ball.startBall()
                self.madeByFlag = True
                self.gameManager.canSelect = False
            if keys[K_w]:
                self.firstPlayer.movePlayer("UP")
            elif keys[K_s]:
                self.firstPlayer.movePlayer("DOWN")
            if self.selectedMode == "Offline":
                if keys[K_UP]:
                    self.secondPlayer.movePlayer("UP")
                elif keys[K_DOWN]:
                    self.secondPlayer.movePlayer("DOWN")        

            self.surface.fill((0, 0, 0))

            #  Check if game started, if not move the ball
            if self.ball.startBallFlag:
                self.ball.moveBall()
            #  If game did not start, show "Press Enter to start"
            if not self.ball.startBallFlag:
                self.gameManager.startingGameAlert()
                self.buttonMultiPlayer.displayButton()     
                self.buttonOffline.displayButton()           
                self.buttonImpossible.displayButton()
                #  Only for the first time, show "Made By Yuval"
                if not self.madeByFlag:
                    self.gameManager.madeByDisplay()
            #  After first time, show score (and not "Made by Yuval")
            if self.selectedMode == "Impossible":
                impossiblePlayer.moveImpossible()
            self.gameManager.checkCollision()

            self.showScreen()

    def showScreen(self):
            if self.madeByFlag:
                self.gameManager.scoreDisplay()
            if self.selectedMode == "Offline":
                self.buttonOffline.displayState(self.selectedMode)
            elif self.selectedMode == "MultiPlayer":
                self.buttonMultiPlayer.displayState(self.selectedMode)
            elif self.selectedMode == "Impossible":
                self.buttonImpossible.displayState(self.selectedMode)
            
            self.ball.drawBall()
            self.firstPlayer.drawPlayer()
            self.secondPlayer.drawPlayer()
            
            self.image = self.surface.blit((0, 0, 0))
            pygame.display.flip()
