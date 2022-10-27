from xml.dom.minidom import NamedNodeMap
import pygame
from pygame.locals import *

from GameHandlers.button import Button
from GameHandlers.gameManager import GameManager

from Sockets.server import Server


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
        madeByFlag = False
        #  Modes can be "Offline", "MultiPlayer", "Impossible"
        selectedMode = ""
        
        clock = pygame.time.Clock()
    
        gameManager = GameManager()
        firstPlayer = gameManager.firstPlayer
        secondPlayer = gameManager.secondPlayer
        ball = gameManager.ball
        impossiblePlayer = gameManager.impossiblePlayer

        buttonMultiPlayer = Button(r'D:\Yuval_Python\Yuval Final Proj\Game\Images\MultiPlayer.png',
                                     self.WIDTH / 2 + 100, self.HEIGHT / 2 + 100)
        buttonOffline = Button(r'D:\Yuval_Python\Yuval Final Proj\Game\Images\Offline.png', 
                            self.WIDTH / 2 - 100, self.HEIGHT / 2 + 200)
        buttonImpossible = Button(r'D:\Yuval_Python\Yuval Final Proj\Game\Images\Impossible.png', 
                            self.WIDTH / 2 - 300, self.HEIGHT / 2 + 100)
        
        pygame.display.flip()
        while gameFlag:
            clock.tick(120)
            for event in pygame.event.get():

                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    cursorX, cursorY = pygame.mouse.get_pos()
                    if gameManager.canSelect:
                        if buttonImpossible.checkPressed(cursorX, cursorY):
                            selectedMode = "Impossible"
                            gameManager.resetScore()
                        elif buttonMultiPlayer.checkPressed(cursorX, cursorY):
                            selectedMode = "MultiPlayer"
                            gameManager.resetScore()
                        elif buttonOffline.checkPressed(cursorX, cursorY):
                            selectedMode = "Offline" 
                            gameManager.resetScore()

                if event.type == QUIT:
                    gameFlag = False

            keys = pygame.key.get_pressed()

            if keys[K_RETURN]:
                ball.startBall()
                madeByFlag = True
                gameManager.canSelect = False
            if keys[K_w]:
                firstPlayer.movePlayer("UP")
            elif keys[K_s]:
                firstPlayer.movePlayer("DOWN")
            if selectedMode == "Offline":
                if keys[K_UP]:
                    secondPlayer.movePlayer("UP")
                elif keys[K_DOWN]:
                    secondPlayer.movePlayer("DOWN")        

            self.surface.fill((0, 0, 0))

            #  Check if game started, if not move the ball
            if ball.startBallFlag:
                ball.moveBall()
            #  If game did not start, show "Press Enter to start"
            if not ball.startBallFlag:
                gameManager.startingGameAlert()
                buttonMultiPlayer.displayButton()     
                buttonOffline.displayButton()           
                buttonImpossible.displayButton()
                #  Only for the first time, show "Made By Yuval"
                if not madeByFlag:
                    gameManager.madeByDisplay()
            #  After first time, show score (and not "Made by Yuval")
            if madeByFlag:
                gameManager.scoreDisplay()
            if selectedMode == "Offline":
                buttonOffline.displayState(selectedMode)
            elif selectedMode == "MultiPlayer":
                buttonMultiPlayer.displayState(selectedMode)
            elif selectedMode == "Impossible":
                buttonImpossible.displayState(selectedMode)
            if selectedMode == "Impossible":
                impossiblePlayer.moveImpossible()
            gameManager.checkCollision()
            ball.drawBall()
            firstPlayer.drawPlayer()
            secondPlayer.drawPlayer()
            
            pygame.display.flip()


GUI()